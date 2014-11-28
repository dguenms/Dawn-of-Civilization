# Rhye's and Fall of Civilization - Constants
# globals

from CvPythonExtensions import *
gc = CyGlobalContext()

iWorldX = 124
iWorldY = 68

# initialise player variables to player IDs from WBS
iNumPlayers = 43
(iEgypt, iChina, iBabylonia, iGreece, iIndia, iCarthage, iPolynesia, iPersia, iRome, iTamils, 
iEthiopia, iKorea, iMaya, iByzantium, iJapan, iVikings, iArabia, iTibet, iKhmer, iIndonesia, 
iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, iMali, iPoland, iPortugal, iInca, 
iItaly, iMongolia, iAztecs, iMughals, iTurkey, iThailand, iCongo, iNetherlands, iGermany, iAmerica, 
iArgentina, iBrazil, iCanada) = range(iNumPlayers)

(pEgypt, pChina, pBabylonia, pGreece, pIndia, pCarthage, pPolynesia, pPersia, pRome, pTamils,
pEthiopia, pKorea, pMaya, pByzantium, pJapan, pVikings, pArabia, pTibet, pKhmer, pIndonesia,
pMoors, pSpain, pFrance, pEngland, pHolyRome, pRussia, pMali, pPoland, pPortugal, pInca,
pItaly, pMongolia, pAztecs, pMughals, pTurkey, pThailand, pCongo, pNetherlands, pGermany, pAmerica,
pArgentina, pBrazil, pCanada) = [gc.getPlayer(i) for i in range(iNumPlayers)]

(teamEgypt, teamChina, teamBabylonia, teamGreece, teamIndia, teamCarthage, teamPolynesia, teamPersia, teamRome, teamTamils,
teamEthiopia, teamKorea, teamMaya, teamByzantium, teamJapan, teamVikings, teamArabia, teamTibet, teamKhmer, teamIndonesia,
teamMoors, teamSpain, teamFrance, teamEngland, teamHolyRome, teamRussia, teamMali, teamPoland, teamPortugal, teamInca,
teamItaly, teamMongolia, teamAztecs, teamMughals, teamTurkey, teamThailand, teamCongo, teamNetherlands, teamGermany, teamAmerica,
teamArgentina, teamBrazil, teamCanada) = [gc.getTeam(i) for i in range(iNumPlayers)]

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
iSeljuks = iNumPlayers+4
iNumTotalPlayers = iNumPlayers+5
iBarbarian = iNumPlayers+5
iNumTotalPlayersB = iBarbarian+1

l0Array =       [0 for i in range(iNumPlayers)]
l0ArrayActive = [0 for i in range(iNumPlayers)]
l0ArrayTotal =  [0 for i in range(iNumTotalPlayers)]

lm1Array =      [-1 for i in range(iNumPlayers)]

# civilizations, not players
iNumCivilizations = 57
(iCivAmerica, iCivArabia, iCivAztec, iCivArgentina, iCivBabylonia, iCivBrazil, iCivByzantium, iCivCanada, iCivCarthage, iCivCelt, 
iCivChina, iCivColombia, iCivEgypt, iCivEngland, iCivEthiopia, iCivFrance, iCivGermany, iCivGreece, iCivHarappa, iCivHolyRoman, 
iCivInca, iCivIndia, iCivIndonesia, iCivIran, iCivItaly, iCivJapan, iCivKhmer, iCivKongo, iCivKorea, iCivMali, 
iCivMaya, iCivMexico, iCivMongol, iCivMoors, iCivMughals, iCivNativeAmericans, iCivNetherlands, iCivOttomans, iCivPersia, iCivPoland, 
iCivPolynesia, iCivPortugal, iCivRome, iCivRussia, iCivSeljuks, iCivSpain, iCivSumeria, iCivTamils, iCivThailand, iCivTibet, 
iCivViking, iCivZulu, iCivIndependent, iCivIndependent2, iCivNative, iCivMinor, iCivBarbarian) = range(iNumCivilizations)

#for Congresses and Victory
lCivGroups = [[iGreece, iRome, iByzantium, iVikings, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iItaly, iPoland, iPortugal, iGermany],  #Euros
                [iIndia, iChina, iPolynesia, iPersia, iJapan, iTamils, iKorea, iByzantium, iTibet, iKhmer, iIndonesia, iRussia, iMongolia, iMughals, iThailand], #Asian
                [iEgypt, iBabylonia, iPersia, iByzantium, iArabia, iTurkey, iCarthage], #MiddleEastern
                [iEgypt, iGreece, iCarthage, iRome, iByzantium, iMoors], #Mediterranean
                [iEgypt, iCarthage, iEthiopia, iMali, iCongo], #African
                [iMaya, iInca, iAztecs, iAmerica, iArgentina, iBrazil, iCanada]] #American

lCivStabilityGroups = [[iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany],  #Euros
                [iIndia, iChina, iPolynesia, iJapan, iKorea, iTibet, iKhmer, iIndonesia, iMongolia, iThailand, iTamils], #Asian
                [iBabylonia, iPersia, iArabia, iTurkey, iMughals], #MiddleEastern
                [iEgypt, iGreece, iCarthage, iRome, iEthiopia, iByzantium, iMoors, iMali, iCongo], #Mediterranean
                [iMaya, iInca, iAztecs, iAmerica, iArgentina, iBrazil, iCanada]] #American
		
lTechGroups = [[iRome, iGreece, iByzantium, iVikings, iSpain, iFrance, iEngland, iHolyRome, iRussia, iNetherlands, iPoland, iPortugal, iItaly, iGermany, iAmerica, iArgentina, iBrazil, iCanada], #Europe and NA
	       [iEgypt, iBabylonia, iIndia, iCarthage, iPersia, iEthiopia, iArabia, iMoors, iMali, iTurkey, iMughals, iTamils, iCongo], #Middle East
	       [iChina, iKorea, iJapan, iTibet, iKhmer, iIndonesia, iMongolia, iThailand], #Far East
	       [iPolynesia, iMaya, iInca, iAztecs]] #Native America


lCivBioOldWorld = [iEgypt, iIndia, iChina, iBabylonia, iGreece, iPolynesia, iPersia, iCarthage, iRome, iJapan, iTamils, 
                   iEthiopia, iKorea, iByzantium, iVikings, iArabia, iTibet, iKhmer, iIndonesia, iMoors, iSpain, iFrance, iEngland, iHolyRome, iRussia, 
                   iNetherlands, iMali, iTurkey, iPoland, iPortugal, iItaly, iMongolia, iAmerica, iMughals, iThailand, iCongo, iGermany, 
                   iIndependent, iIndependent2, iCeltia, iBarbarian]
lCivBioNewWorld = [iMaya, iInca, iAztecs] #, iNative]


#for Victory and the handler
tAmericasTL = (3, 0)
tAmericasBR = (43, 63)

# Colombian UP
tSouthCentralAmericaTL = (13, 3)
tSouthCentralAmericaBR = (41, 39)

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
[iBabylonia, iGreece, iPersia, iCarthage, iRome, iEthiopia, iByzantium, iArabia, iMoors, iTurkey], #Egypt
[iIndia, iJapan, iKorea, iTibet, iKhmer, iMongolia, iThailand], #China
[iEgypt, iGreece, iPersia, iTurkey, iMongolia, iCarthage, iByzantium], #Babylonia
[iPersia, iCarthage, iRome, iByzantium, iHolyRome, iRussia, iTurkey, iItaly], #Greece
[iChina, iPersia, iTamils, iTibet, iKhmer, iMongolia, iMughals, iThailand], #India
[iEgypt, iGreece, iRome, iSpain, iMali, iPortugal, iBabylonia, iPersia, iArabia, iMoors, iTurkey, iItaly], #Carthage
[], # Polynesia
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
[iAmerica], #Canada
]

#for stability hit on spawn
lOlderNeighbours = [
[], #Egypt
[], #China
[], #Babylonia
[iEgypt, iBabylonia], #Greece
[], #India
[iEgypt, iBabylonia], #Carthage
[], # Polynesia
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
[iPersia, iGreece, iByzantium], #Russia
[iCarthage, iEthiopia, iArabia, iMoors], #Mali
[iVikings, iHolyRome], #Poland
[iCarthage, iRome], #Portugal
[], #Inca
[iByzantium, iHolyRome], #Italy
[iChina, iJapan, iKorea, iArabia, iTibet, iKhmer, iRussia], #Mongolia
[iMaya], #Aztec
[iIndia, iPersia, iArabia, iTibet], #Mughals
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
1271,					# China
-539,					# Babylonia
-146,					# Greece
600, # end of Gupta Empire		# India
-146,					# Phoenicia
1200,					# Polynesia
651,					# Persia
235, # crisis of the third century	# Rome
1200,					# Tamils
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

tVictoryYears = (
(-850, -100, 170), # Egypt
(1000, -1, 1800), # China
(-1, -850, -700), # Babylonia
(-1, -250, -330), # Greece
(-1, 700, 1200), # India
(-300, -100, 200), # Carthage
(800, 1000, 1200), # Polynesia
(140, 350, 350), # Persia
(100, 320, -1), # Rome
(800, 1000, 1200), # Tamils
(-1, 600, 1910), # Ethiopia
(1200, -1, -1), # Korea
(600, 900, -1), # Maya
(1000, 1200, 1450), # Byzantium
(1600, 1940, -1), # Japan
(1050, 1100, 1500), # Vikings
(1300, 1300, -1), # Arabia
(1000, 1400, 1700), # Tibet
(1200, 1450, 1450), # Khmer
(1300, 1500, 1940), # Indonesia
(1200, 1300, 1650), # Moors
(-1, 1650, 1700), # Spain
(1700, 1800, 1900), # France
(1730, 1800, -1), # England
(1200, -1, 1700), # HolyRome
(1920, -1, 1950), # Russia
(1350, 1500, 1700), # Mali
(1400, -1, 1600), # Poland
(1550, 1650, 1700), # Portugal
(1500, 1550, 1700), # Inca
(1500, 1600, 1930), # Italy
(1300, -1, 1500), # Mongolia
(1520, 1650, -1), # Aztecs
(1500, 1660, 1750), # Mughals
(1550, 1700, 1800), # Turkey
(1650, 1700, 1900), # Thailand
(1650, 1800, -1), # Congo
(1650, 1750, 1800), # Iran
(1745, 1745, 1775), # Holland
(1900, 1940, -1), # Germany
(1930, 2000, 2000), # America
(1880, 1940, 1960), # Mexico
(1900, 1930, 1960), # Argentina
(1870, 1920, 1950), # Colombia
(1880, -1, 1950), # Brazil
(   -1,  -1,   -1), # Canada
)

# Leoreth: date-triggered respawn for certain civs
tRebirth = (
-1,				# Egypt
-1,				# China
-1,				# Babylonia
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
-1)		# Canada

tRebirthPlot = (
-1,		# Egypt
-1,		# China
-1,		# Babylonia
(69,44),	# Greece
(88,36),	# Marathas - Raigad/Mumbai # India
-1,		# Phoenicia
-1,		# Polynesia
(81,41),	# Safavids - Esfahan # Persia
(59,46),	# Italy - Florence # Rome
-1,		# Tamils
-1,		# Ethiopia
-1,		# Korea
(27, 29),	# Gran Colombia - Bogota # Maya
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
-1,		# Brazil
-1)		# Canada
		
tRebirthArea = (
-1,			# Egypt
-1,			# China
-1,			# Babylonia
((64,45),(74,42)),	# Byzantium - Balkans, Greece, Anatolia, Levant # Greece
((87,28),(94,37)),	# Maratha - Deccan	# India
-1,			# Phoenicia
-1,			# Polynesia
((78,38),(86,43)),	# Safavids - Azerbaijan, Iran, Afghanistan (no Merv, no Baghdad) # Persia
((57,45),(62,47)),	# Italy - Lombardy and Tuscany without Rome
-1,			# Tamils
-1,			# Ethiopia
-1,			# Korea
((23, 25), (31, 32)),	# Gran Colombia - Ecuador, Colombia, Venezuela, Panama
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
-1,			# Brazil
-1)			# Canada

dRebirthExceptions = {
iAztecs : ((17, 48), (18, 48), (19, 48), (20, 48), (21, 48), (22, 48), (23, 48), (18, 47), (19, 47), (20, 47), (21, 47), (22, 47), (23, 47), (18, 46), (19, 46), (20, 46), (21, 46), (22, 46), (23, 46), (21, 45), (22, 45), (23, 45), (22, 44), (23, 44), (22, 43), (23, 43), (23, 42), (22, 35), (21, 34), (22, 34), (23, 34)),
}

tResurrectionIntervals = (
[(900, 1300), (1800, 2020)], #Egypt
[(600, 2020)], #China
[(-3000, -500)], #Babylonia
[(1800, 2020)], #Greece
[(1900, 2020)], #India
[(-1000, -150)], #Carthage
[],		# Polynesia
[(220, 650), (1500, 2020)], #Persia
[(-750, 450)], #Rome
[(-300, 600)], #Tamils
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
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_MARATHON", "TXT_KEY_UHV_GRE3_MARATHON"),
("TXT_KEY_UHV_IND1_MARATHON", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3_MARATHON"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2_MARATHON", "TXT_KEY_UHV_KON3"),
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
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_EPIC", "TXT_KEY_UHV_GRE3_EPIC"),
("TXT_KEY_UHV_IND1_EPIC", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3_EPIC"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2_EPIC", "TXT_KEY_UHV_KON3"),
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
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2", "TXT_KEY_UHV_KON3"),
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
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_NOTURN", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3_MARATHON"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2_MARATHON", "TXT_KEY_UHV_KON3"),
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
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2_NOTURN", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3_EPIC"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2_EPIC", "TXT_KEY_UHV_KON3"),
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
("TXT_KEY_UHV_GRE1", "TXT_KEY_UHV_GRE2", "TXT_KEY_UHV_GRE3"),
("TXT_KEY_UHV_IND1", "TXT_KEY_UHV_IND2", "TXT_KEY_UHV_IND3"),
("TXT_KEY_UHV_CAR1", "TXT_KEY_UHV_CAR2", "TXT_KEY_UHV_CAR3"),
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
("TXT_KEY_UHV_KON1", "TXT_KEY_UHV_KON2", "TXT_KEY_UHV_KON3"),
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
(("TXT_KEY_URV_PRO1", "TXT_KEY_URV_PRO2", "TXT_KEY_URV_PRO3"),
("TXT_KEY_URV_CAT1_MARATHON", "TXT_KEY_URV_CAT2", "TXT_KEY_URV_CAT3"),
("TXT_KEY_URV_ORT1", "TXT_KEY_URV_ORT2", "TXT_KEY_URV_ORT3"),
("TXT_KEY_URV_ISL1", "TXT_KEY_URV_ISL2", "TXT_KEY_URV_ISL3"),
("TXT_KEY_URV_HIN1", "TXT_KEY_URV_HIN2_MARATHON", "TXT_KEY_URV_HIN3"),
("TXT_KEY_URV_BUD1_MARATHON", "TXT_KEY_URV_BUD2_MARATHON", "TXT_KEY_URV_BUD3"),
("TXT_KEY_URV_CON1", "TXT_KEY_URV_CON2", "TXT_KEY_URV_CON3"),
("TXT_KEY_URV_TAO1_MARATHON", "TXT_KEY_URV_TAO2", "TXT_KEY_URV_TAO3"),
("TXT_KEY_URV_ZOR1", "TXT_KEY_URV_ZOR2", "TXT_KEY_URV_ZOR3"),
("TXT_KEY_URV_POL1", "TXT_KEY_URV_POL2", "TXT_KEY_URV_POL3"),
("TXT_KEY_URV_SEC1", "TXT_KEY_URV_SEC2", "TXT_KEY_URV_SEC3")),
# Epic
(("TXT_KEY_URV_PRO1", "TXT_KEY_URV_PRO2", "TXT_KEY_URV_PRO3"),
("TXT_KEY_URV_CAT1_EPIC", "TXT_KEY_URV_CAT2", "TXT_KEY_URV_CAT3"),
("TXT_KEY_URV_ORT1", "TXT_KEY_URV_ORT2", "TXT_KEY_URV_ORT3"),
("TXT_KEY_URV_ISL1", "TXT_KEY_URV_ISL2_EPIC", "TXT_KEY_URV_ISL3"),
("TXT_KEY_URV_HIN1", "TXT_KEY_URV_HIN2", "TXT_KEY_URV_HIN3"),
("TXT_KEY_URV_BUD1_EPIC", "TXT_KEY_URV_BUD2_EPIC", "TXT_KEY_URV_BUD3"),
("TXT_KEY_URV_CON1", "TXT_KEY_URV_CON2", "TXT_KEY_URV_CON3"),
("TXT_KEY_URV_TAO1_EPIC", "TXT_KEY_URV_TAO2", "TXT_KEY_URV_TAO3"),
("TXT_KEY_URV_ZOR1", "TXT_KEY_URV_ZOR2", "TXT_KEY_URV_ZOR3"),
("TXT_KEY_URV_POL1", "TXT_KEY_URV_POL2", "TXT_KEY_URV_POL3"),
("TXT_KEY_URV_SEC1", "TXT_KEY_URV_SEC2", "TXT_KEY_URV_SEC3")),
# Normal
(("TXT_KEY_URV_PRO1", "TXT_KEY_URV_PRO2", "TXT_KEY_URV_PRO3"),
("TXT_KEY_URV_CAT1", "TXT_KEY_URV_CAT2", "TXT_KEY_URV_CAT3"),
("TXT_KEY_URV_ORT1", "TXT_KEY_URV_ORT2", "TXT_KEY_URV_ORT3"),
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
iBabylonia	:	"TXT_KEY_DOM_BABYLONIA",
iGreece		:	"TXT_KEY_DOM_GREECE",
iCarthage	:	"TXT_KEY_DOM_PHOENICIA",
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
iPersia		:	"TXT_KEY_DOM_PERSIA_1700AD",
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
(4, 18), #Tonga
(82, 38), #tPersepolis
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
(59, 51), #Frankfurt
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
(62, 53), #Berlin
(27, 46), #tWashington
(34, 11), #Buenos Aires
(41, 18), #Rio de Janeiro
(30, 52), #Montreal
),
((69, 33), #tThebes
(102, 47), #tBeijing
(76, 40), #tBabylon
(67, 41), #tAthens
(90, 40), #tDelhi
(58, 39), #tCarthage
#(73, 40), #tSur
(4, 18), #Tonga
(81, 41), #Esfahan
(60, 44), #tRome
(91, 31), #Thanjavur
(72, 29), #tAksum
(109, 46), #tSeoul
(27, 29), #Bogota
(68, 45), #tConstantinople
(113, 45), #tKyoto
#(61, 62), #tNidaros
(60, 59), #tOslo
(75, 33), #tMecca
(96, 43), #Lhasa
#(102, 34), #tAngkor
(101, 37), #Hanoi
(100, 26), #Palembang
(51, 41), #Cordoba
(52, 44), #tMadrid
(55, 50), #tParis
(53, 54), #tLondon
#(62, 52), #tBerlin
(62, 49), #tVienna
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
(62, 53), #Berlin
(27, 46), #tWashington
(34, 11), #Buenos Aires
(41, 18), #Rio de Janeiro
(29, 50), #Ottawa
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
(),
)

# birth areas (flipped on spawn)

tBirthAreaTL = (
(66, 30), #Egypt
(99, 43), #China 
(75, 39), #Babylonia
(65, 39), #Greece
(87, 36), #India
(71, 39), #Carthage
(3, 17), #Polynesia
(79, 37), #Persia
(59, 41), #Rome
(90, 28), #Tamils
(69, 27), #Ethiopia
(107, 45), #Korea
(20, 35), #Maya
(64, 38), #Byzantium
(111, 41), #Japan
(58, 56), #Vikings
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
(31, 3), #Buenos Aires
(36, 15), #Brazil
(20, 50), #Canada
)

tBirthAreaBR = (
(70, 36), #Egypt
(107, 47), #China
(77, 42), #Babylonia
(70, 45), #Greece
(96, 40), #India
(74, 41), #Carthage
(7, 22), #Polynesia
(85, 44), #Persia
(63, 47), #Rome
(93, 34), #Tamils
(73, 30), #Ethiopia
(110, 49), #Korea
(23, 37), #Maya
(74, 45), #Byzantium
(116, 49), #Japan
(64, 62), #Vikings
(80, 40), #Arabia	81,39
(98, 45), #Tibet
(103, 36), #Khmer
(107, 31), #Indonesia
(58, 43), #Moors
(53, 46), #Spain
(57, 52), #France
(54, 60), #England   57 without Scotland
(64, 54), #Holy Rome
(74, 58), #Russia
(57, 31), #Mali
(67, 55), #Poland
(50, 44), #Portugal
(29, 24), #Inca
(63, 47), #Italy
(105, 54), #Mongolia
(20, 41), #Aztecs
(91, 43), #Mughals
(76, 48), #Turkey
(103, 36), #Thailand
(65, 22), #Congo
(58, 54), #Holland
(65, 55), #Germany
(32, 50), #America
(35, 13), #Argentina
(43, 27), #Brazil
(35, 60), #Canada
)

tBirthAreaExceptions = (
(), #Egypt
((106, 47)), #China
((78, 41), (78, 42)), #Babylonia
((64, 45), (65, 45), (66, 45)), #Greece
(), #India
(),#(73, 40), (73, 41)), #Carthage
(), #Polynesia
((72, 39), (72, 40), (72, 41), (73, 41), (74, 41), (75, 41), (76, 41), (77, 41), (78, 41), (73, 40), (74, 40), (75, 40), (76, 40), (77, 40), (78, 40), (73, 39), (74, 39), (75, 39), (76, 39), (77, 39), (78, 39), (73, 38), (74, 38), (75, 38), (76, 38), (77, 38), (72, 37), (73, 37), (74, 37), (75, 37), (76, 37), (77, 37), (78, 37)), #Persia
(), #Rome
((90, 33), (90, 34), (91, 34)), #Tamils
(), #Ethiopia
(), #Korea
(), #Maya
(), #Byzantium
(), #Japan
(), #Vikings
((82, 34), (73, 40), (75, 40), (71, 36), (72, 37), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30), (72, 30), (72, 31), (72, 32), (71, 32)),  #Arabia
((98, 42),), #Tibet
(), #Khmer
((100, 31), (100, 30), (101, 29)), #Indonesia
((58, 43), (58, 42)), #Moors
((49, 41), (49, 42), (49, 43), (49, 44), (50, 43), (50, 44), (50, 42)), #Spain
((55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46), (56, 52), (57, 52)), #France
(), #England
((64, 51), (64, 52), (64, 53), (64, 54)),  #Holy Rome
((68, 58), (69, 58), (70, 58), (65, 55), (66, 55), (66, 56)), #Russia
(), #Mali
((63, 50), (64, 50)), #Poland
(), #Portugal
(), #Inca
((63,47), (63,46)), #Italy
((99, 47), (100, 47), (101, 47), (102, 47), (103, 47), (99, 46), (100, 46), (101, 46), (102, 46), (103, 46), (104, 46), (99, 45), (100, 45), (101, 45), (102, 45), (103, 45), (104, 45), (105, 45), (106, 45)), #Mongolia
(), #Aztecs
((92, 43), (93, 42), (93, 43), (94, 42), (94, 43)), #Mughals
((74, 48), (75, 48), (76, 48), (75, 47), (75, 48), (76, 41)), #Turkey
(), #Thailand
(), #Congo
((57, 51), (58, 51)), #Holland
((62, 49), (62, 50), (63, 49), (63, 50), (64, 49), (64, 50), (64, 51), (65, 49), (65, 50), (65, 51), (66, 49), (66, 50), (66, 51), (58, 52), (58, 53), (62, 51), (63, 51), (64, 53), (61, 49), (61, 50), (64, 52), (58, 54), (65, 52), (65, 53)),  #Germany
((25, 48), (25, 49), (25, 50), (26, 48), (26, 49), (27, 49), (27, 50), (28, 50), (29, 50), (30, 50)), #America
((35, 4), (35, 12), (35, 13), (36, 12), (36, 13)), #Argentina
((36, 15), (36, 16)), #Brazil
((20, 50), (21, 50), (22, 50), (23, 50), (24, 50), (25, 50), (29, 50), (30, 50), (31, 50), (32, 50), (20, 51), (21, 51), (22, 51), (23, 51), (24, 51), (32, 51), (35, 53), (35, 54), (34, 55), (34, 56), (33, 56), (33, 57)), #Canada
)

#core areas (for RiseAndFall and Victory)

tCoreAreasTL = (
((67, 32), #Egypt
(99, 43), #China 
(75, 39), #Babylonia
(64, 39), #Greece
(90, 38), #India
(73, 39), #Carthage
(3, 17), #Polynesia
(79, 37), #Persia
(59, 41), #Rome
(90, 28), #Tamils
(69, 27), #Ethiopia
(108, 45), #Korea
(20, 35), #Maya
(64, 40), #Byzantium
(112, 45), #Japan
(58, 56), #Vikings
(73, 30), #Arabia
(92, 41), #Tibet
(100, 32), #Khmer
(98, 24), #Indonesia
(51, 37), #Moors
(49, 43), #Spain
(51, 46), #France
(50, 53), #England
(58, 48), #Holy Rome
(68, 49), #Russia
(51, 28), #Mali
(63, 50), #Poland
(44, 42), #Portugal
(26, 20), #Inca
(58, 45), #Italy
(95, 47), #Mongolia
(16, 35), #Aztecs
(86, 38), #Mughals
(69, 42), #Turkey
(100, 32), #Thailand
(61, 19), #Congo
(56, 52), #Holland
(58, 49), #Germany
(23, 45), #America
(31, 6), #Argentina
(37, 15), #Brazil
(27, 50), #Canada
),
((67, 32), #Egypt
(99, 41), #China 
(75, 39), #Babylonia
(65, 39), #Greece
(90, 38), #India
(54, 37), #Carthage
(3, 17), #Polynesia
(79, 37), #Persia
(58, 45), #Rome	
(90, 28), #Tamils
(69, 27), #Ethiopia
(108, 45), #Korea
(24, 26), #Colombia
(67, 44), #Byzantium
(111, 41), #Japan
(58, 56), #Vikings
(73, 38), #Arabia
(92, 41), #Tibet
(97, 35), #Khmer (Vietnam)
(98, 24), #Indonesia
(51, 37), #Moors
(49, 40), #Spain
(51, 46), #France
(50, 53), #England
(61, 46), #Holy Rome
(68, 49), #Russia
(51, 28), #Mali
(63, 50), #Poland
(44, 42), #Portugal
(26, 20), #Inca
(58, 40), #Italy
(95, 46), #Mongolia
(16, 35), #Mexico
(86, 37), #Mughals
(67, 42), #Turkey
(100, 32), #Thailand
(61, 19), #Congo
(56, 52), #Holland
(58, 49), #Germany
(23, 45), #America
(31, 6), #Argentina
(37, 15), #Brazil
(27, 50), #Canada
)) 

tCoreAreasBR = (
((69, 36), #Egypt
(107, 47), #China
(77, 42), #Babylonia
(70, 45), #Greece
(96, 40), #India
(74, 41), #Carthage
(7, 22), #Polynesia
(85, 44), #Persia
(63, 47), #Rome
(93, 34), #Tamils
(73, 30), #Ethiopia
(109, 48), #Korea
(23, 37), #Maya
(72, 46), #Byzantium
(116, 47), #Japan
(64, 62), #Vikings
(76, 38), #Arabia
(98, 45), #Tibet
(103, 36), #Khmer
(107, 31), #Indonesia
(53, 42), #Moors
(53, 46), #Spain
(57, 51), #France
(54, 60), #England   57 without Scotland
(64, 54), #Holy Rome
(75, 59), #Russia
(57, 32), #Mali
(67, 55), #Poland
(50, 44), #Portugal
(29, 24), #Inca
(63, 47), #Italy
(105, 52), #Mongolia
(19, 38), #Aztecs
(91, 43), #Mughals
(76, 46), #Turkey
(103, 36), #Thailand
(65, 22), #Congo
(58, 54), #Holland
(65, 55), #Germany
(32, 50), #America
(35, 12), #Argentina
(41, 22), #Brazil
(35, 52), #Canada
),
((69, 36), #Egypt
(107, 47), #China
(77, 42), #Babylonia
(69, 42), #Greece
(96, 40), #India
(60, 39), #Carthage
(7, 22), #Polynesia
(85, 44), #Persia
(63, 47), #Rome
(93, 34), #Tamils
(73, 30), #Ethiopia
(109, 48), #Korea
(31, 32), #Colombia
(69, 46), #Byzantium
(116, 49), #Japan
(64, 62), #Vikings
(78, 42), #Arabia
(98, 45), #Tibet
(102, 38), #Khmer
(107, 31), #Indonesia
(56, 39), #Moors
(55, 46), #Spain
(57, 51), #France
(54, 60), #England   57 without Scotland
(66, 51), #Holy Rome
(75, 59), #Russia
(57, 32), #Mali
(67, 55), #Poland
(50, 44), #Portugal
(29, 24), #Inca
(63, 47), #Italy
(106, 49), #Mongolia
(19, 40), #Mexico
(94, 43), #Mughals
(76, 47), #Turkey
(103, 36), #Thailand
(65, 22), #Congo
(58, 54), #Holland
(63, 55), #Germany
(32, 50), #America
(35, 12), #Argentina
(41, 22), #Brazil
(35, 52), #Canada
))


tExceptions = (  #for RiseAndFall
((), #Egypt
((106, 47)), #China
((78, 41), (78, 42)), #Babylonia
((64, 45), (65, 45), (66, 45)), #Greece
(), #India
(),#(73, 40), (73, 41)), #Carthage
(), #Polynesia
((72, 39), (72, 40), (72, 41), (73, 41), (74, 41), (75, 41), (76, 41), (77, 41), (78, 41), (73, 40), (74, 40), (75, 40), (76, 40), (77, 40), (78, 40), (73, 39), (74, 39), (75, 39), (76, 39), (77, 39), (78, 39), (73, 38), (74, 38), (75, 38), (76, 38), (77, 38), (72, 37), (73, 37), (74, 37), (75, 37), (76, 37), (77, 37), (78, 37)), #Persia
(), #Rome
((90, 33), (90, 34), (91, 34)), #Tamils
(), #Ethiopia
(), #Korea
(), #Maya
((71, 40)), #Byzantium
(), #Japan
(), #Vikings
((82, 34), (73, 40), (75, 40), (71, 36), (72, 37), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30), (72, 30), (72, 31), (72, 32), (71, 32)),  #Arabia
((98, 42),), #Tibet
(), #Khmer
((100, 31), (100, 30), (101, 29)), #Indonesia
((58, 43), (58, 42)), #Moors
((49, 41), (49, 42), (49, 43), (49, 44), (50, 43), (50, 44), (50, 42)), #Spain
((55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46), (56, 52), (57, 52)), #France
(), #England
((64, 51), (64, 52), (64, 53), (64, 54)),  #Holy Rome
((68, 49), (69, 49), (71, 49), (68, 59), (69, 59), (70, 59), (69, 58)), #Russia
(), #Mali
((63, 50), (64, 50)), #Poland
(), #Portugal
(), #Inca
((63,47), (63,46)), #Italy
((102, 47), (103, 47)), #Mongolia
(), #Aztecs
((92, 43), (93, 42), (93, 43), (94, 42), (94, 43)), #Mughals
(), #Turkey
(), #Thailand
(), #Congo
((57, 51), (58, 51)), #Holland
((62, 49), (62, 50), (63, 49), (63, 50), (64, 49), (64, 50), (64, 51), (65, 49), (65, 50), (65, 51), (66, 49), (66, 50), (66, 51), (58, 52), (58, 53), (62, 51), (63, 51), (64, 53), (61, 49), (61, 50), (64, 52), (58, 54), (65, 52), (65, 53)),  #Germany
((23, 50), (24, 50), (27, 50), (28, 50), (29, 50), (30, 50), (27, 49)), #America
((35, 12)), #Argentina
(), #Brazil
((29, 50), (30, 50), (31, 50), (31, 50), (32, 50), (32, 51)), #Canada
),
((), #Egypt
((99, 41), (106, 47)), #China
((78, 41), (78, 42)), #Babylonia
((64, 45), (65, 45), (66, 46)), #Greece
(), #India
(),#(73, 40), (73, 41)), #Carthage
(), #Polynesia
(), #Persia
((63,47), (63,46)), #Rome		# ITALY
((90, 33), (90, 34), (91, 34)), #Tamils
(), #Ethiopia
(), #Korea
((30, 26), (31, 26), (30, 27), (31, 27), (30, 28), (30, 29)), #Colombia
((71, 40)), #Byzantium
(), #Japan
(), #Vikings
((82, 34), (73, 40), (75, 40), (71, 36), (72, 37), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30), (72, 30), (72, 31), (72, 32), (71, 32)),  #Arabia
((98, 42),), #Tibet
(), #Khmer
((100, 31), (100, 30), (101, 29)), #Indonesia
((58, 43), (58, 42)), #Moors
((49, 41), (49, 42), (49, 43), (49, 44), (50, 43), (50, 44), (50, 42), (55, 46)), #Spain
((55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46)), #France
(), #England
((61, 51), (64, 51), (65, 51), (66, 51)),  #HolyRome
((68, 49), (69, 49), (71, 49), (68, 59), (69, 59), (70, 59), (69, 58)), #Russia
(), #Mali
((63, 50), (64, 50)), #Poland
(), #Portugal
(), #Inca
((63,47), (63,46)), #Italy
(), #Mongolia
((19, 40)), #Mexico
((92, 43)), #Mughals
((68, 48), (68, 49), (73, 40), (73, 41), (73, 42), (71, 42), (70, 42), (74, 42), (75, 42), (80, 47), (80, 48), (80, 49), (67, 42)), #Turkey
(), #Thailand
(), #Congo
((57, 51), (58, 51)), #Holland
((62, 49), (62, 50), (63, 49), (63, 50), (64, 49), (64, 50), (64, 51), (65, 49), (65, 50), (65, 51), (66, 49), (66, 50), (66, 51), (62, 51), (63, 51), (66, 52), (65, 53), (66, 53), (65, 52)),  #Germany
((23, 50), (24, 50), (27, 50), (28, 50), (29, 50), (30, 50), (27, 49)), #America
((35, 12)), #Argentina
(), #Brazil
((29, 50), (30, 50), (31, 50), (31, 50), (32, 50), (32, 51)), #Canada
))



#normal areas (for Victory and resurrection)

tNormalAreasTL = (
((65, 30), #Egypt
(99, 39), #China
(74, 38), #Babylonia
(64, 39), #Greece
(87, 28), #India
(72, 39), #Carthage
(3, 15), #Polynesia
(79, 37), #Persia
(57, 40), #Rome
(90, 28), #Tamils
(68, 25), #Ethiopia
(108, 45), #Korea
(20, 32), #Maya
(64, 40), #Byzantium
(111, 41), #Japan
(58, 56), #Vikings
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
( 8, 50), #Canada
),
((65, 30), #Egypt
(99, 39), #China
(74, 38), #Babylonia
(64, 39), #Greece
(86, 29), #India
(71, 39), #Carthage
(3, 15), #Polynesia
(79, 37), #Persia
(57, 40), #Rome
(90, 28), #Tamils
(68, 25), #Ethiopia
(108, 45), #Korea
(24, 26), #Colombia
(64, 40), #Byzantium
(111, 41), #Japan
(58, 56), #Vikings
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
( 8, 50), #Canada
))

tNormalAreasBR = (
((72, 37), #Egypt
(108, 50), #China
(79, 44), #Babylonia
(68, 44), #Greece
(94, 37), #India
(74, 41), #Carthage
(13, 21), #Polynesia
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
(69, 55), #Poland
(50, 44), #Portugal
(30, 29), #Inca
(63, 47), #Italy
(104, 54), #Mongolia
(20, 40), #Aztecs
(94, 43), #Mughals
(78, 49), #Turkey
(103, 37), #Thailand
(65, 22), #Congo
(58, 54), #Holland
(66, 55), #Germany
(31, 49), #America
(36, 15), #Argentina
(43, 28), #Brazil
(37, 67), #Canada
),
((72, 37), #Egypt
(108, 50), #China
(79, 44), #Babylonia
(68, 44), #Greece
(97, 42), #India
(74, 41), #Carthage
(13, 21), #Polynesia
(86, 46), #Persia
(63, 47), #Rome
(93, 34), #Tamils
(77, 30), #Ethiopia
(110, 49), #Korea
(29, 32), #Colombia
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
(69, 55), #Poland
(50, 44), #Portugal
(30, 29), #Inca
(63, 47), #Italy
(104, 54), #Mongolia
(20, 40), #Aztecs
(94, 43), #Mughals
(78, 49), #Turkey
(103, 37), #Thailand
(65, 22), #Congo
(58, 54), #Holland
(66, 55), #Germany
(31, 49), #America
(36, 15), #Argentina
(43, 28), #Brazil
(37, 67), #Canada
))


tNormalAreasSubtract = (  #for resurrection and stability
(((72, 37), (70, 30), (71, 30), (72, 30)), #Egypt
((99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50), (100, 39), (101, 39)), #China
(), #Babylonia
(), #Greece
((93, 42), (94, 42), (95, 42), (96, 42)), #India
(), #Carthage
((13, 21),), #Polynesia
((86, 39), (86, 38), (86, 37)), #Persia
((62, 47), (63, 47), (63, 46)), #Rome
(), #Tamils
((76, 30), (77, 30)), #Ethiopia
(), #Korea
(), #Maya
(), #Byzantium
((111, 52), (112, 52), (111, 51)), #Japan
((65, 56), (66, 56), (67, 56), (66, 57), (67, 57)), #Vikings
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
((11,50), (12,50), (13,50), (14,50), (16,50), (17,50), (18,50), (19,50), (20,50), (21,50), (22,50), (23,50), (24,50), (25,50), (29,50), (30,50), (31,50), (32,50), (32,51), (8,59), (8,60), (8,61), (8,62), (8,63), (8,64), (8,65), (9,59), (9,60), (9,61), (9,62), (9,63), (9,64), (9,65), (37,66), (37,67)), #Canada 
),
(((72, 37), (70, 30), (71, 30), (72, 30)), #Egypt
((99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50)), #China
(), #Babylonia
(), #Greece
((93, 42), (94, 42), (95, 42), (96, 42)), #India
(), #Carthage
((13, 21),), #Polynesia
((86, 39), (86, 38), (86, 37)), #Persia
((62, 47), (63, 47), (63, 46)), #Rome
(), #Tamils
((76, 30), (77, 30)), #Ethiopia
(), #Maya
(), #Byzantium
((111, 52), (112, 52), (111, 51)), #Japan
((65, 56), (66, 56), (67, 56), (66, 57), (67, 57)), #Vikings
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
((11,50), (12,50), (13,50), (14,50), (16,50), (17,50), (18,50), (19,50), (20,50), (21,50), (22,50), (23,50), (24,50), (25,50), (29,50), (30,50), (31,50), (32,50), (32,51), (8,59), (8,60), (8,61), (8,62), (8,63), (8,64), (8,65), (9,59), (9,60), (9,61), (9,62), (9,63), (9,64), (9,65), (37,66), (37,67)), #Canada 
))

# broader areas coordinates (top left and bottom right) (for RiseAndFall)

tBroaderAreasTL = (
((60, 26), #Egypt
(95, 38), #China
(72, 37), #Babylonia
(62, 39), #Greece
(85, 28), #India
(71, 39), #Carthage
(1, 15), #Polynesia
(70, 37), #Persia
(49, 35), #Rome
(90, 28), #Tamils
(67, 21), #Ethiopia
(106, 45), #Korea
(19, 30), #Maya
(58, 34), #Byzantium
(110, 40), #Japan
(58, 56), #Vikings
(64, 30), #Arabia
(92, 41), #Tibet
(97, 25), #Khmer
(98, 24), #Indonesia
(51, 37), #Moors
(49, 38), #Spain
(49, 44), #France
(48, 53), #England
(58, 43), #Holy Rome
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
( 8, 50), #Canada
),
((60, 26), #Egypt
(95, 38), #China
(72, 37), #Babylonia
(62, 39), #Greece
(85, 28), #India
(71, 39), #Carthage
(1, 15), #Polynesia
(70, 37), #Persia
(57, 47), #Rome		# ITALY
(90, 28), #Tamils
(67, 21), #Ethiopia
(106, 45), #Korea
(33, 32), #Colombia
(64, 38), #Byzantium
(110, 40), #Japan
(58, 56), #Vikings
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
(84, 37), #Mughals
(68, 42), #Turkey
(97, 25), #Thailand
(61, 19), #Congo
(56, 51), #Holland
(55, 46), #Germany
(10, 42), #America
(29,  3), #Argentina
(32, 14), #Brazil
( 8, 50), #Canada
))

tBroaderAreasBR = (
((74, 38), #Egypt
(108, 50), #China
(78, 44), #Babylonia
(77, 47), #Greece
(99, 43), #India
(74, 41), #Carthage
(17, 38), #Polynesia
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
(64, 54), #Holy Rome
(92, 59), #Russia
(67, 32), #Mali
(67, 55), #Poland
(51, 45), #Portugal
(30, 27), #Inca
(65, 47), #Italy
(110, 62), #Mongolia
(24, 43), #Aztecs
(94, 43), #Mughals
(86, 49), #Turkey
(105, 39), #Thailand
(65, 22), #Congo
(58, 54), #Holland
(67, 57), #Germany
(37, 56), #America
(36, 15), #Argentina
(43, 28), #Brazil
(37, 67), #Canada
),
((74, 38), #Egypt
(108, 50), #China
(78, 44), #Babylonia
(77, 47), #Greece
(99, 43), #India
(74, 41), #Carthage
(17, 38), #Polynesia
(87, 49), #Persia
(65, 47), #Rome		# ITALY
(93, 34), #Tamils
(77, 30), #Ethiopia
(110, 52), #Korea
(33, 32), #Colombia
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
(67, 55), #Poland
(51, 45), #Portugal
(30, 27), #Inca
(65, 47), #Italy
(110, 62), #Mongolia
(24, 43), #Aztecs
(94, 43), #Mughals
(86, 49), #Turkey
(105, 39), #Thailand
(65, 22), #Congo
(58, 54), #Holland
(67, 57), #Germany
(37, 56), #America
(36, 15), #Argentina
(43, 28), #Brazil
(37, 67), #Canada
))

# Leoreth: new capital locations if changed during the game
tNewCapitals = (
-1,		# Egypt
-1,		# China
-1,		# Babylonia
-1,		# Greece
-1,		# India
-1,		# Phoenicia
-1,		# Polynesia
-1,		# Persia
-1,		# Rome
-1,		# Tamils
-1,		# Ethiopia
-1,		# Korea
-1,		# Maya
-1,		# Byzantium
(116, 46), #Tokyo
(63, 59), #Stockholm
-1,		# Arabia
-1,		# Tibet
-1,		# Khmer
-1,		# Indonesia
-1,		# Moors
-1,		# Spain
-1,		# France
-1,		# England
(62, 49), #Vienna
-1,		# Russia
-1,		# Mali
-1,		# Poland
-1,		# Portugal
-1,		# Inca
(59, 41), #Rome	# Italy
(102, 47), # Khanbaliq
-1,		# Aztecs
-1,		# Mughals
(68, 45), #Istanbul
-1,		# Thailand
-1,		# Congo
-1,		# Netherlands
-1,		# Germany
-1,		# America
-1, 		# Argentina
-1,		# Brazil
-1)		# Canada

#Leoreth: respawn areas and capitals similar to SoI
tRespawnCapitals = (
(69, 35), #Al-Qahira
(102, 47), #Beijing
-1,		# Babylonia
-1,		# Greece
(90, 40), #Delhi
-1,		# Phoenicia
-1,		# Polynesia
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
(51, 37), #Marrakesh
-1,		# Spain
-1,		# France
-1,		# England
(62, 49), #Vienna
-1,		# Russia
-1,		# Mali
-1,		# Poland
-1,		# Portugal
(26, 22), #Lima
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
-1,		# Brazil
-1)		# Canada

# area flipped on respawn, if -1 normal area is used instead
tRespawnTL = (
(65, 30), #Egypt
(99, 39), #China
-1,		# Babylonia
-1,		# Greece
(88, 33),	# India
-1,		# Phoenicia
-1,		# Polynesia
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
(48, 34), #Moors
-1,		# Spain
-1,		# France
-1,		# England
-1,		# Holy Rome
-1,		# Russia
-1,		# Mali
-1,		# Poland
-1,		# Portugal
(25, 16), # Peru
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
-1,		# Brazil
-1)		# Canada

tRespawnBR = (
(71, 39), 	# Egypt
(107, 47), 	# China
-1,		# Babylonia
-1,		# Greece
(96, 41), 	# India
-1,		# Phoenicia
-1,		# Polynesia
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
(58, 39), #Moors
-1,		# Spain
-1,		# France
-1,		# England
-1,		# Holy Rome
-1,		# Russia
-1,		# Mali
-1,		# Poland
-1,		# Portugal
(33, 25), # Peru
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
-1,		# Brazil
-1)		# Canada

# starting gold in 3000 BC
tStartingGold = (
0,	# Egypt
0,	# China
0,	# Babylonia
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

#rnf. Some civs have a double entry, for a higher chance
lEnemyCivsOnSpawn = [
[], #Egypt
[iIndependent,iIndependent2,iIndependent2], #China
[iIndependent,iIndependent2], #Babylonia
[iIndependent,iIndependent2,iBabylonia], #Greece
[], #India
[], #Carthage
[], #Polynesia
[iBabylonia,iBabylonia,iGreece,iCarthage,iCarthage,iIndia,iIndia], #Persia
#[iEgypt,iGreece,iGreece,iCarthage,iCarthage], #Rome
[], # rome for testing
[], #Tamils
[], #Ethiopia
[], #Korea
[], #Maya
[iGreece, iPersia], #Byzantium
[], #Japan
[iEngland,iEngland,iFrance,iIndependent,iIndependent2], #Vikings
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
[iSpain, iSpain, iIndependent,iIndependent2], #Argentina
[iIndependent,iIndependent2], #Brazil
[], #Canada
]

# Leoreth
lTotalWarOnSpawn = [
[], #Egypt
[], #China
[], #Babylonia
[], #Greece
[], #India
[], #Phoenicia
[], #Polynesia
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
[], #Canada
]


#AIWars
tAggressionLevel = (
0, #Egypt
1, #China
1, #Babylonia
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
iAesthetics, iSailing, iWriting, iMathematics, iAlphabet, iCalendar, iCurrency, iPhilosophy, iPaper, iBanking, 
iEducation, iPrintingPress, iEconomics, iAstronomy, iChemistry, iScientificMethod, iPhysics, iBiology, iMedicine, iElectricity,
iCombustion, iFission, iFlight, iAdvancedFlight, iPlastics, iComposites, iStealth, iGenetics, iFiberOptics, iFusion,
iHunting, iMining, iArchery, iMasonry, iAnimalHusbandry, iBronzeWorking, iHorsebackRiding, iIronWorking, iMetalCasting, iCompass, 
iConstruction, iMachinery, iEngineering, iOptics, iGunpowder, iReplaceableParts, iMilitaryScience, iRifling, iSteamPower, iSteel, 
iAssemblyLine, iRailroad, iArtillery, iIndustrialism, iRadio, iRefrigeration, iSuperconfuctors, iComputers, iLaser, iRocketry, 
iSatellites, iRobotics) = range(iNumTechs)

iUtopia = iCommunism

iFutureTech = iNumTechs
iNumTechsFuture = iNumTechs+1


# initialise unit variables to unit indices from XML

iNumUnits = 152
(iLion, iBear, iPanther, iWolf, iSettler, iWorker, iIndianFastWorker, iBrazilianLenhador, iScout, iExplorer, iSpy, iJewishMissionary,
iChristianMissionary, iOrthodoxMissionary, iIslamicMissionary, iHinduMissionary, iBuddhistMissionary, iConfucianMissionary, iTaoistMissionary,
iZoroastrianMissionary, iWarrior, iIncanQuechua, iHarappanMilitia, iSwordsman, iAztecJaguar, iCelticGallicWarrior, iRomePraetorian,
iAxeman, iGreekPhalanx, iSumerianVulture, iNativeAmericaDogSoldier, iMaceman, iJapanSamurai, iVikingBerserker, iKongoPombos, 
iSpearman, iZuluImpi, iPikeman, iHolyRomanLandsknecht, iMusketman, iFrenchMusketeer, iOttomanJanissary, iEthiopianOromoWarrior, 
iIranianQizilbash, iIroquoisMohawk, iRifleman, iEnglishRedcoat, iAmericanMinuteman, iGrenadier, iColombianAlbionLegion, iAtInfantry, iInfantry, iBersagliere,
iSamInfantry, iMobileSam, iMarine, iAmericanNavySeal, iParatrooper, iMechanizedInfantry, iArcher, iMaliSkirmisher, iBabylonBowman, iNubianMedjay, iMayaHolkan, 
iLongbowman, iCrossbowman, iChinaChokonu, iChariot, iEgyptWarChariot, iCelticCidainh, iHittiteHuluganni, iPersiaImmortal, iHorseArcher, iCarthageNumidianCavalry, 
iKushanAsvaka, iMongolKeshik, iTibetanKhampa, iKnight, iArabiaCamelarcher, iByzantineCataphract, iSeljukGhulamWarrior, iThaiChangSuek, iMandeFarari, 
iSpanishConquistador, iCuirassier,  iMoorishCamelGunner, iPolishWingedHussar, iSiouxMountedBrave, iCavalry, iRussiaCossack, iMexicoRurales, iArgentineGrenadierCavalry, 
iWarElephant, iKhmerBallistaElephant, iCarthaginianWarElephant, iTank, iGermanPanzer, iModernArmor, iGunship, iCatapult, iKoreanHwacha, iTrebuchet, 
iBombard, iMughalSiegeElephant, iCannon, iFrenchHeavyCannon, iMachineGun, iArtillery, iMobileArtillery, iWorkboat, iGalley, iPolynesianWaka, iBireme, iTrireme, iCaravel, 
iPortugalCarrack, iTamilDharani, iGalleon, iNetherlandsOostindievaarder, iPrivateer, iIndonesianOrangLaut, iMoorishCorsair, iFrigate, iShipOfTheLine, 
iIronclad, iTransport,  iDestroyer, iCanadaCorvette,iBattleship, iMissileCruiser, iStealthDestroyer, iSubmarine, iAttackSubmarine, iCarrier, iAirship, iFighter, iJetFighter, 
iBomber, iStealthBomber, iGuidedMissile, iTacticalNuke, iIcbm, iProphet, iArtist, iScientist, iMerchant, iEngineer, iGreatGeneral, iGreatSpy,
iSlave, iNativeSlave, iAztecSlave) = range(iNumUnits)

iCongoPombos = iKongoPombos
iCamelArcher = iArabiaCamelarcher
iConquistador = iSpanishConquistador
iWorkBoat = iWorkboat
iHeavySwordsman = iMaceman
iEthiopianAskari = iEthiopianOromoWarrior
iDutchEastIndiaman = iNetherlandsOostindievaarder

# initialise bonuses variables to bonuses IDs from WBS
iNumBonuses = 40
(iAluminium, iCoal, iCopper, iHorse, iIron, iMarble, iOil, iStone, iUranium, iBanana, iClam, iCorn, iCow, iCrab,
iDeer, iFish, iPig, iRice, iSheep, iWheat, iDye, iFur, iGems, iGold, iIncense, iIvory, iSilk, iSilver, iSpices,
iSugar, iWine, iWhales, iSoccer, iSongs, iMovies, iCotton, iCoffee, iTea, iTobacco, iPearls) = range(iNumBonuses)

#Buildings (update Persian UHV every time this is changed)

iNumBuildings = 207
(iPalace, iGreatPalace, iForbiddenPalace, iWalls, iCelticDun, iCastle, iSpanishCitadel, iIncanTambo, iBarracks, iZuluIkhanda, iStable,
iMongolGer, iBunker, iBombShelter, iGranary, iIncanTerrace, iAqueduct, iOttomanHammam, iKhmerBaray, iIndianStepwell, iMoorishNoria, iHarappanBath,
iHospital, iRecyclingCenter, iLighthouse, iVikingTradingPost, iHarbor, iCustomHouse, iPortugalFeitoria, iDrydock, iAirport,
iForge, iMaliMint, iItalianArtStudio, iFactory, iGermanAssemblyPlant, iCoalPlant, iJapaneseShalePlant, iHydroPlant, iNuclearPlant,
iIndustrialPark, iObelisk, iEgyptianObelisk, iEthiopianStele, iNativeAmericaTotem, iIndonesianCandi, iPublicTransportation, iAcademy,
iLibrary, iArabianMadrassa, iChineseTaixue, iThaiHoTrai, iTamilSangam, iUniversity, iKoreanSeowon, iTibetanGompa, iObservatory, iLaboratory, 
iRussianResearchInstitute, iTheatre, iGreekOdeon, iByzantineHippodrome, iChinesePavillion, iColosseum, iMayaBallCourt, iBabylonGarden, iMexicoCharreada, 
iPolynesianMarae, iBroadcastTower, iMarket, iRomanForum, iPersianApothecary, iIranianCaravanserai, iKongoMbwadi, iPhoenicianGlassmaker, 
iGrocer, iBrazilianFazenda, iColombianHacienda, iBank, iEnglishStockExchange, iSupermarket, iAmericanMall, iArgentineRefrigerationPlant, iCourthouse,
iAztecSacrificialAltar,  iHolyRomanRathaus, iSumerianZiggurat, iPolishSejmik, iJail, iIndianMausoleum, iFrenchSalon, iCanadianRoyalMountedPolice, iLevee, 
iNetherlandsDike, iIntelligenceAgency, iNationalSecurity, iJewishTemple, iJewishCathedral, iJewishMonastery, iJewishShrine, iChristianTemple, iChristianCathedral, 
iChristianMonastery, iChristianShrine, iOrthodoxTemple, iOrthodoxCathedral, iOrthodoxMonastery, iOrthodoxShrine, iIslamicTemple, iIslamicCathedral,
iIslamicMonastery, iIslamicShrine, iHinduTemple, iHinduCathedral, iHinduMonastery, iHinduShrine, iBuddhistTemple, 
iBuddhistCathedral, iBuddhistMonastery, iBuddhistShrine, iConfucianTemple, iConfucianCathedral, iConfucianMonastery,
iConfucianShrine, iTaoistTemple, iTaoistCathedral, iTaoistMonastery, iTaoistShrine, iZoroastrianTemple, iZoroastrianCathedral,
iZoroastrianMonastery, iZoroastrianShrine, iTriumphalArch, iGlobeTheatre, iNationalPark, iNationalGallery,
iWallStreet, iIronWorks, iTradingCompany, iIberianTradingCompany, iRedCross, iInterpol, iMilitaryAcademy, iPyramid,
iStonehenge, iGreatLibrary, iGreatLighthouse, iHangingGarden, iColossus, iOracle, iParthenon, iFlavianAmphitheatre, iAngkorWat,
iTempleOfKukulkan, iSistineChapel, iSpiralMinaret, iNotreDame, iTajMahal, iKremlin, iEiffelTower, iStatueOfLiberty,
iWembley, iGraceland, iHollywood, iGreatDam, iPentagon, iMtRushmore, iUnitedNations, iSpaceElevator, iCERN, iArtemis,
iSankore, iGreatWall, iStatueOfZeus, iMausoleumOfMaussollos, iCristoRedentor, iShwedagonPaya, iGreatCothon, iMoaiStatues, iApostolicPalace,
iLeaningTower, iOlympicPark, iTempleOfSalomon, iIshtarGate, iTheodosianWalls, iTerracottaArmy, iMezquita, iDomeOfTheRock,
iTopkapiPalace, iBrandenburgGate, iSanMarcoBasilica, iWestminster, iBorobudur, iKhajuraho,
iHimejiCastle, iPorcelainTower, iHarmandirSahib, iBlueMosque, iRedFort, iVersailles, iTrafalgarSquare, iEmpireState,
iGrandCanal, iFloatingGardens, iLubyanka, iMachuPicchu, iCNTower) = range(iNumBuildings)

iBeginWonders = iPyramid # different from DLL constant because that includes national wonders

iSummerPalace = iGreatPalace
iHeroicEpic = iFlavianAmphitheatre
iNationalEpic = iTriumphalArch
iHermitage = iNationalGallery 
iScotlandYard = iInterpol
iChichenItza = iTempleOfKukulkan
iBroadway = iWembley
iRocknroll = iGraceland
iThreeGorgesDam = iGreatDam
iChannelTunnel = iCERN

iPaganTemple = iObelisk

iTemple = iJewishTemple #generic
iCathedral = iJewishCathedral #generic
iMonastery = iJewishMonastery #generic
iShrine = iJewishShrine #generic

iPlague = iNumBuildings
iNumBuildingsPlague = iNumBuildings+1

iNumBuildingsEmbassy = iNumBuildingsPlague+iNumPlayers
(iEgyEmbassy, iChiEmbassy, iBabEmbassy, iGreEmbassy, iIndEmbassy, iCarEmbassy, iPlyEmbassy, iPerEmbassy, iRomEmbassy, iTamEmbassy, iEthEmbassy, 
iKorEmbassy, iMayEmbassy, iByzEmbassy, iJapEmbassy, iVikEmbassy, iAraEmbassy, iTibEmbassy, iKhmEmbassy, iInoEmbassy, iMooEmbassy, iSpaEmbassy,
iFraEmbassy, iEngEmbassy, HreEmbassy, iRusEmbassy, iMalEmbassy, iPolEmbassy, iPorEmbassy, iIncEmbassy, iItaEmbassy, iMonEmbassy, 
iAztEmbassy, iMugEmbassy, iTurEmbassy, iThaEmbassy, iConEmbassy, iHolEmbassy, iGerEmbassy, iAmeEmbassy, iArgEmbassy, iBraEmbassy, iCanEmbassy) = range(iNumBuildingsPlague, iNumBuildingsPlague+iNumPlayers)

#Civics
iNumCivics = 36
(iCivicTyranny, iCivicDynasticism, iCivicCityStates, iCivicTheocracy, iCivicAutocracy, iCivicRepublic,
iCivicDirectRule, iCivicVassalage, iCivicAbsolutism, iCivicRepresentation, iCivicTotalitarianism, iCivicEgalitarianism,
iCivicTribalism, iCivicSlavery, iCivicAgrarianism, iCivicCapitalism, iCivicIndustrialism, iCivicPublicWelfare,
iCivicSelfSufficiency, iCivicGuilds, iCivicMercantilism, iCivicFreeMarket, iCivicCentralPlanning, iCivicEnvironmentalism,
iCivicAnimism, iCivicPantheon, iCivicOrganizedReligion, iCivicScholasticism, iCivicFanaticism, iCivicSecularism,
iCivicMilitia, iCivicWarriorCode, iCivicMercenaries, iCivicLevyArmies, iCivicStandingArmy, iCivicNavalDominance) = range(iNumCivics)

#Specialists
iNumSpecialists = 15
(iCitizen, iSpecialistPriest, iSpecialistArtist, iSpecialistScientist, iSpecialistMerchant, iSpecialistEngineer, iSpecialistSpy, iGreatProphet, iGreatArtist, iGreatScientist, iGreatMerchant,
iGreatEngineer, iGreatGeneral, iSpecialistGreatSpy, iSettledSlave) = range(iNumSpecialists)

#Stability Levels
iNumStabilityLevels = 5
(iStabilityCollapsing, iStabilityUnstable, iStabilityShaky, iStabilityStable, iStabilitySolid) = range(iNumStabilityLevels)

#Stability Types
iNumStabilityTypes = 5
(iStabilityExpansion, iStabilityEconomy, iStabilityDomestic, iStabilityForeign, iStabilityMilitary) = range(iNumStabilityTypes)

#Stability Parameters
iNumStabilityParameters = 21
(iParameterCorePeriphery, iParameterCoreScore, iParameterPeripheryScore, iParameterRazedCities,						# Expansion
iParameterEconomicGrowth, iParameterTrade, iParameterMercantilism, iParameterCentralPlanning,						# Economy
iParameterHappiness, iParameterCivicCombinations, iParameterCivicsEraTech, iParameterReligion,						# Domestic
iParameterNeighbors, iParameterVassals, iParameterDefensivePacts, iParameterRelations, iParameterAutocracy, iParameterFanaticism,	# Foreign
iParameterWarSuccess, iParameterWarWeariness, iParameterBarbarianLosses) = range(iNumStabilityParameters)				# Military

#Stability Display
#iNumStabilityTypes = 44
#(iStabilityDiplomacy, iStabilityNeighbor, iStabilityVassal, iStabilityImperialism, iStabilityContacts, iStabilityExpansion, iStabilityOuterExpansion,
#iStabilityOccupiedCore, iStabilityCivics, iStabilityCivicEra, iStabilityCivicCities, iStabilityCivicCap, iStabilityCivicTech, iStabilityForeignCoreCities,
#iStabilityCityHappiness, iStabilityCityCivics, iStabilityCityCulture, iStabilityCityTotal, iStabilityTrade, iStabilityEconomy, iStabilityHappiness,
#iStabilityEconomyExtra, iStabilityGreatDepression, iStabilityForeignGreatDepression, iStabilityPostCommunism, iStabilityDemocracyTransition, 
#iStabilityNumCities, iStabilityCombat, iStabilityCombatExtra, iStabilityAnarchy, iStabilityGoldenAge, iStabilityFall, iStabilityBase, iStabilityNormalization,
#iStabilityCitiesBuilt, iStabilityCitiesLost, iStabilityCitiesConquered, iStabilityCitiesRazed, iStabilityTech, iStabilityBuildings,
#iStabilityReligion, iStabilityDifficulty, iStabilityCap, iStabilityHit) = range(iNumStabilityTypes)

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

iNumProjects = 12
(iManhattanProject, iTheInternet, iSDI, iApolloProgram, iSSCasing, iSSThrusters, iSSEngine, iSSDockingBay,
iSSCockpit, iSSLifeSupport, iSSStasisChamber, iPersecutionProject) = range(iNumProjects)


#Eras

iNumEras = 7
(iAncient, iClassical, iMedieval, iRenaissance, iIndustrial, iModern, iFuture) = range (iNumEras)


#Improvements

iNumImprovements = 27
(iLandWorked, iWaterWorked, iCityRuins, iHut, iFarm, iFishingBoats, iHighSeaFishingBoats, iWhalingBoats, iMine, iWorkshop, iLumbermill, iWindmill, iWatermill, iPlantation, 
iSlavePlantation, iQuarry, iPasture, iCamp, iWell, iOffshorePlatform, iWinery, iCottage, iHamlet, iVillage, iTown, iFort, iForestPreserve) = range(iNumImprovements)

#feature & terrain

iSeaIce = 0
iJungle = 1
iOasis = 2
iFloodPlains = 3
iForest = 4
iFallout = 5
iMud = 6
iCape = 7

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
iVictoryPolytheism = 9
iVictorySecularism = 10


#leaders

iNumLeaders = 112
(iLeaderBarbarian, iAlexander, iAsoka, iAugustus, iBismarck, iBoudica, iBrennus, iCatherine, iCharlemagne, iChurchill,
iCyrus, iDarius, iDeGaulle, iElizabeth, iFrederick, iGandhi, iGenghisKhan, iGilgamesh, iHammurabi, iHannibal, iHatshepsut,
iHuaynaCapac, iIsabella, iJoao, iJuliusCaesar, iJustinian, iKublaiKhan, iLincoln, iLouis, iMansaMusa, iMao,
iMehmed, iMontezuma, iNapoleon, iPacal, iPericles, iPeter, iQinShiHuang, iRamesses, iRagnar, iFranklinRoosevelt,
iSaladin, iShaka, iSittingBull, iStalin, iSuleiman, iSuryavarman, iTokugawa, iVictoria, iWangKon, iWashington, iWillemVanOranje, 
iZaraYaqob, iJimmu, iMeiji, iAkbar, iHiram, iHaileSelassie, iGustav, iAbuBakr, iMongkut, iElishat,
iPhilip, iBarbarossa, iCharles, iFrancis, iYaroslav, iAfonso, iAtaturk, iMaria, iHitler, iFranco, iNicholas, iCixi,
iChiangKaishek, iCavour, iAbbas, iKhomeini, iTaizong, iHongwu, iDharmasetu, iHayamWuruk, iSuharto, iShivaji,
iNaresuan, iAlpArslan, iBaibars, iNasser, iAlfred, iTrudeau, iChandragupta, iTughluq, iBasil, iRahman, iRajendra, iLobsangGyatso,
iSobieski, iVatavelli, iMbemba, iHarun, iSongtsen, iCasimir, iYaqub, iLorenzo, iSantaAnna, iJuarez, iCardenas, iDomPedro, 
iSanMartin, iPeron, iBolivar, iAhoeitu) = range(iNumLeaders)

iCleopatra = iHatshepsut
iSargon = iGilgamesh
iOdaNobunaga = iTokugawa

resurrectionLeaders = {
	iChina : iHongwu,
	iIndia : iShivaji,
	iEgypt : iBaibars,
}

rebirthLeaders = {
	iMaya : iBolivar,
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
0,	# Polynesia
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
1,	# Canada
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

lSecondaryCivs = [iPolynesia, iTamils, iTibet, iMoors, iPoland, iCongo, iArgentina, iBrazil]

(i3000BC, i600AD, i1700AD) = range(3)

tLatestActiveScenario = (
i3000BC, 	# Egypt
i1700AD,	# China
i3000BC,	# Babylonia
i3000BC,	# Greece
i3000BC,	# India
i3000BC,	# Phoenicia
i3000BC,	# Polynesia
i3000BC,	# Persia
i3000BC,	# Rome
i3000BC,	# Tamils
i3000BC,	# Ethiopia
i1700AD,	# Korea
i3000BC,	# Maya
i600AD,		# Byzantium
i1700AD,	# Japan
i1700AD,	# Vikings
i600AD,		# Arabia
i600AD,		# Tibet
i600AD,		# Khmer
i600AD,		# Indonesia
i600AD,		# Moors
i1700AD,	# Spain
i1700AD,	# France
i1700AD,	# England
i1700AD,	# Holy Rome
i1700AD,	# Russia
i600AD,		# Mali
i1700AD,	# Poland
i1700AD,	# Portugal
i600AD,		# Inca
i600AD,		# Italy
i600AD,		# Mongolia
i600AD,		# Aztecs
i1700AD,	# Mughals
i1700AD,	# Turkey
i1700AD,	# Thailand
i1700AD,	# Congo
i1700AD,	# Netherlands
i1700AD,	# Germany
i1700AD,	# America
i1700AD,	# Argentina
i1700AD,	# Brazil
i1700AD,	# Canada
i1700AD,	# Independent
i1700AD,	# Independent
i1700AD,	# Natives
i3000BC,	# Celts
i600AD)		# Seljuks