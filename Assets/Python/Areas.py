from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]

def isReborn(iPlayer):
	return gc.getPlayer(iPlayer).isReborn()
	
def getOrElse(dDictionary, key, default):
	if key in dDictionary: return dDictionary[key]
	return default
	
def getArea(iPlayer, tRectangle, dExceptions, bReborn=None, dChangedRectangle={}, dChangedExceptions={}):
	if bReborn is None: bReborn = isReborn(iPlayer)
	tBL, tTR = tRectangle[iPlayer]
	lExceptions = getOrElse(dExceptions, iPlayer, [])
	
	if bReborn:
		if iPlayer in dChangedRectangle:
			tBL, tTR = dChangedRectangle[iPlayer]
			lExceptions = getOrElse(dChangedExceptions, iPlayer, [])
	
	left, bottom = tBL
	right, top = tTR		
	return [(x, y) for x in range(left, right+1) for y in range(bottom, top+1) if (x, y) not in lExceptions]

def getCapital(iPlayer, bReborn=None):
	if bReborn is None: bReborn = isReborn(iPlayer)
	if bReborn and iPlayer in dChangedCapitals:
		return dChangedCapitals[iPlayer]
	return tCapitals[iPlayer]
	
def getRespawnCapital(iPlayer, bReborn=None):
	if iPlayer in dRespawnCapitals: return dRespawnCapitals[iPlayer]
	return getCapital(iPlayer, bReborn)
	
def getNewCapital(iPlayer, bReborn=None):
	if iPlayer in dNewCapitals: return dNewCapitals[iPlayer]
	return getRespawnCapital(iPlayer, bReborn)
	
def getBirthArea(iPlayer):
	return getArea(iPlayer, tBirthArea, dBirthAreaExceptions)
	
def getBirthRectangle(iPlayer, bExtended = None):
	if bExtended is None: bExtended = isExtendedBirth(iPlayer)
	if iPlayer in dChangedBirthArea and isExtendedBirth(iPlayer):
		return dChangedBirthArea[iPlayer]
	return tBirthArea[iPlayer]
	
def getCoreArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tCoreArea, dCoreAreaExceptions, bReborn, dChangedCoreArea, dChangedCoreAreaExceptions)
	
def getNormalArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tNormalArea, dNormalAreaExceptions, bReborn, dChangedNormalArea, dChangedNormalAreaExceptions)

def getBroaderArea(iPlayer, bReborn=None):
	return getArea(iPlayer, tBroaderArea, {}, dChangedBroaderArea)
	
def getRespawnArea(iPlayer):
	if iPlayer in dRespawnArea: return getArea(iPlayer, dRespawnArea, {})
	return getNormalArea(iPlayer)
	
def getRebirthArea(iPlayer):
	if iPlayer in dRebirthArea: return getArea(iPlayer, dRebirthArea, dRebirthAreaExceptions)
	return getBirthArea(iPlayer)
	
def updateCore(iPlayer):
	lCore = getCoreArea(iPlayer)
	for x in range(iWorldX):
		for y in range(iWorldY):
			plot = gc.getMap().plot(x, y)
			if plot.isWater() or (plot.isPeak() and (x, y) not in lPeakExceptions): continue
			plot.setCore(iPlayer, (x, y) in lCore)
			
def isForeignCore(iPlayer, tPlot):
	x, y =  tPlot
	plot = gc.getMap().plot(x, y)
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer == iPlayer: continue
		if plot.isCore(iLoopPlayer):
			return True
	return False
	
def isExtendedBirth(iPlayer):
	if gc.getGame().getActivePlayer() == iPlayer: return False
	
	# add special conditions for extended AI flip zones here
	if iPlayer == iTurkey and pByzantium.isAlive(): return False
	
	return True
			
def init():
	for iPlayer in range(iNumPlayers):
		updateCore(iPlayer)
	
### Capitals ###

tCapitals = (
(69, 33), # Thebes
(100, 44), # Chang'an
(76, 40), # Babylon
(87, 40), # Harappa
(67, 41), # Athens
(94, 40), # Pataliputra
(73, 40), # Sur
(4, 18), # Tonga
(82, 38), # Persepolis
(60, 44), # Rome
(91, 30), # Thanjavur
(72, 29), # Aksum
(109, 46), # Seoul
(22, 35), # Tikal
(68, 45), # Constantinople
(113, 45), # Kyoto
(60, 59), # Oslo
(75, 33), # Mecca
(96, 43), # Lhasa
(102, 33), # Angkor
(100, 26), # Palembang
(51, 41), # Cordoba
(52, 44), # Madrid
(55, 50), # Paris
(53, 54), # London
(59, 51), # Frankfurt
(73, 54), # Moskow
(53, 31), # Timbuktu
(65, 51), # Krakow
(49, 43), # Lisboa
(28, 22), # Cuzco
(59, 46), # Florence
(99, 51), # Karakorum
(18, 37), # Tenochtitlan
(90, 40), # Delhi
(70, 43), # Sogut
(101, 33), # Ayutthaya
(62, 20), # Mbanza Kongo
(57, 53), # Amsterdam
(62, 53), # Berlin
(27, 46), # Washington
(34, 11), # Buenos Aires
(41, 18), # Rio de Janeiro
(30, 52), # Montreal
)

dChangedCapitals = {
iChina : (102, 47),	# Beijing
iIndia : (90, 40),	# Delhi
iPhoenicia : (58, 39),	# Carthage
iPersia : (81, 41),	# Esfahan (Iran)
iTamils : (90, 30),	# Vijayanagara
iMaya : (27, 29),	# Bogota (Colombia)
iKhmer : (101, 37),	# Hanoi
iHolyRome : (62, 49),	# Vienna
}

# new capital locations if changed during the game
dNewCapitals = {
iJapan : (116, 46),	# Tokyo
iVikings : (63, 59),	# Stockholm
iHolyRome : (62, 49),	# Vienna
iItaly : (59, 41),	# Rome
iMongolia : (102, 47),	# Khanbaliq
iTurkey : (68, 45),	# Istanbul
}

# new capital locations on respawn
dRespawnCapitals = {
iEgypt : (69, 35),	# Cairo
iChina : (102, 47),	# Beijing
iIndia : (90, 40),	# Delhi
iPersia : (81, 41),	# Esfahan
iEthiopia : (72, 36),	# Addis Ababa
iJapan : (116, 46),	# Tokyo
iVikings : (63, 58),	# Stockholm
iIndonesia : (104, 25),	# Jakarta
iMoors : (51, 37),	# Marrakesh
iHolyRome : (62, 49),	# Vienna
iInca : (26, 22),	# Lima
iItaly : (59, 41),	# Rome
iMughals : (85, 37),	# Karachi
iTurkey : (68, 45),	# Istanbul
}

### Birth Area ###

tBirthArea = (
((66, 30), 	(70, 36)), 	# Egypt
((99, 43), 	(107, 47)), 	# China
((75, 39), 	(77, 42)), 	# Babylonia
((85, 37), 	(88, 41)), 	# Harappa
((65, 39), 	(70, 45)), 	# Greece
((87, 36), 	(96, 40)), 	# India
((71, 39), 	(74, 41)), 	# Carthage
((3, 17), 	(7, 22)), 	# Polynesia
((79, 37), 	(85, 44)), 	# Persia
((59, 41), 	(63, 47)), 	# Rome
((90, 27), 	(93, 32)), 	# Tamils
((69, 27), 	(73, 30)), 	# Ethiopia
((107, 45), 	(110, 49)), 	# Korea
((20, 35), 	(23, 37)), 	# Maya
((64, 38), 	(74, 45)), 	# Byzantium
((111, 41), 	(116, 49)), 	# Japan
((58, 56), 	(64, 62)), 	# Vikings
((67, 30), 	(80, 40)), 	# Arabia
((92, 41), 	(98, 45)), 	# Tibet
((100, 32), 	(103, 36)), 	# Khmer
((98, 24), 	(107, 31)), 	# Indonesia
((51, 37), 	(58, 43)), 	# Moors
((49, 43), 	(53, 46)), 	# Spain
((51, 46), 	(57, 52)), 	# France
((50, 53), 	(54, 60)), 	# England
((58, 48), 	(64, 54)), 	# Holy Rome
((67, 50), 	(74, 58)), 	# Russia
((49, 26), 	(57, 31)), 	# Mali
((63, 50), 	(67, 55)), 	# Poland
((44, 42), 	(50, 44)), 	# Portugal
((26, 20), 	(29, 24)), 	# Inca
((58, 45), 	(63, 47)), 	# Italy
((87, 46), 	(105, 54)), 	# Mongolia
((15, 36), 	(20, 41)), 	# Aztecs
((86, 38), 	(91, 43)), 	# Mughals
((69, 41), 	(76, 48)), 	# Turkey
((100, 32), 	(103, 36)), 	# Thailand
((61, 19), 	(65, 22)), 	# Congo
((56, 52), 	(58, 54)), 	# Holland
((58, 49), 	(65, 55)), 	# Germany
((25, 43), 	(32, 50)), 	# America
((31, 3), 	(35, 13)), 	# Argentina
((36, 15), 	(43, 27)), 	# Brazil
((20, 50), 	(35, 60)), 	# Canada
)

dChangedBirthArea = {
iPersia :	((74, 37), 	(85, 44)), 	# includes Assyria and Anatolia
iSpain : 	((49, 43), 	(55, 46)), 	# includes Catalonia
iInca : 	((26, 19), 	(31, 24)),
iMongolia : 	((81, 45), 	(105, 54)), 	# 6 more west, 1 more south
iTurkey : 	((67, 41), 	(76, 48)), 	# 2 more west
iArgentina : 	((29, 3), 	(35, 13)), 	# includes Chile
}

dBirthAreaExceptions = {
iChina : [(106, 47)],
iBabylonia : [(78, 41), (78, 42)],
iHarappa : [(85, 41), (88, 37), (88, 38)],
iGreece : [(64, 45), (65, 45), (66, 45)],
iPersia : [(85, 37), (85, 38), (85, 39), (72, 39), (72, 40), (72, 41), (73, 41), (74, 41), (75, 41), (76, 41), (77, 41), (78, 41), (73, 40), (74, 40), (75, 40), (76, 40), (77, 40), (78, 40), (73, 39), (74, 39), (75, 39), (76, 39), (77, 39), (78, 39), (73, 38), (74, 38), (75, 38), (76, 38), (77, 38), (72, 37), (73, 37), (74, 37), (75, 37), (76, 37), (77, 37), (78, 37)],
iTamils : [(90, 33), (90, 34), (91, 34)],
iArabia : [(82, 34), (73, 40), (75, 40), (71, 36), (72, 37), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30), (72, 30), (72, 31), (72, 32), (71, 32)],
iTibet : [(98, 42)],
iIndonesia : [(100, 31), (100, 30), (101, 29), (101, 30)],
iMoors : [(58, 43), (58, 42)],
iSpain : [(49, 41), (49, 42), (49, 43), (49, 44), (50, 43), (50, 44), (50, 42)],
iFrance : [(55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46), (56, 52), (57, 52)],
iHolyRome : [(64, 51), (64, 52), (64, 53), (64, 54)],
iRussia : [(68, 58), (69, 58), (70, 58), (65, 55), (66, 55), (66, 56)],
iPoland : [(63, 50), (64, 50)],
iItaly : [(63,47), (63,46)],
iMongolia : [(99, 47), (100, 47), (101, 47), (102, 47), (103, 47), (99, 46), (100, 46), (101, 46), (102, 46), (103, 46), (104, 46), (99, 45), (100, 45), (101, 45), (102, 45), (103, 45), (104, 45), (105, 45), (106, 45)],
iMughals : [(92, 43), (93, 42), (93, 43), (94, 42), (94, 43)],
iTurkey : [(74, 48), (75, 48), (76, 48), (75, 47), (75, 48), (76, 41)],
iNetherlands : [(57, 51), (58, 51)],
iGermany : [(62, 49), (62, 50), (63, 49), (63, 50), (64, 49), (64, 50), (64, 51), (65, 49), (65, 50), (65, 51), (66, 49), (66, 50), (66, 51), (58, 52), (58, 53), (62, 51), (63, 51), (64, 53), (61, 49), (61, 50), (64, 52), (58, 54), (65, 52), (65, 53)],
iAmerica : [(25, 48), (25, 49), (25, 50), (26, 48), (26, 49), (27, 49), (27, 50), (28, 50), (29, 50), (30, 50)],
iArgentina : [(35, 4), (35, 12), (35, 13), (36, 12), (36, 13)],
iBrazil : [(36, 15), (36, 16)],
iCanada : [(20, 50), (21, 50), (22, 50), (23, 50), (24, 50), (25, 50), (29, 50), (30, 50), (31, 50), (32, 50), (20, 51), (21, 51), (22, 51), (23, 51), (24, 51), (32, 51), (35, 53), (35, 54), (34, 55), (34, 56), (33, 56), (33, 57)],
}

### Core Area ###

tCoreArea = (
((67, 32),	(69, 36)),	# Egypt
((99, 43),	(107, 47)),	# China
((75, 39),	(77, 42)),	# Babylonia
((85, 37),	(88, 41)),	# Harappa
((64, 39),	(70, 45)),	# Greece
((90, 38),	(96, 40)),	# India
((73, 39),	(74, 41)),	# Phoenicia
((4, 18),	(6, 21)),	# Polynesia
((79, 37),	(85, 44)),	# Persia
((59, 41),	(63, 47)),	# Rome
((90, 27),	(93, 32)),	# Tamils
((69, 27),	(73, 30)),	# Ethiopia
((108, 45),	(109, 48)),	# Korea
((20, 35),	(23, 37)),	# Maya
((64, 40),	(72, 46)),	# Byzantium
((112, 45),	(116, 47)),	# Japan
((58, 56),	(64, 62)),	# Vikings
((73, 30),	(76, 38)),	# Arabia
((92, 42),	(98, 45)),	# Tibet
((100, 32),	(103, 36)),	# Khmer
((98, 24),	(107, 30)),	# Indonesia
((51, 37),	(53, 42)),	# Moors
((49, 43),	(53, 46)),	# Spain
((51, 46),	(57, 51)),	# France
((50, 53),	(54, 60)),	# England
((58, 48),	(64, 54)),	# HolyRome
((68, 49),	(75, 59)),	# Russia
((51, 28),	(57, 32)),	# Mali
((63, 50),	(67, 55)),	# Poland
((44, 42),	(50, 44)),	# Portugal
((26, 20),	(28, 22)),	# Inca
((58, 45),	(62, 47)),	# Italy
((95, 47),	(105, 52)),	# Mongolia
((16, 35),	(19, 38)),	# Aztecs
((86, 38),	(91, 43)),	# Mughals
((69, 42),	(76, 46)),	# Turkey
((100, 32),	(103, 36)),	# Thailand
((61, 19),	(65, 22)),	# Congo
((56, 52),	(58, 54)),	# Netherlands
((58, 49),	(65, 55)),	# Germany
((23, 45),	(32, 50)),	# America
((31, 6),	(35, 12)),	# Argentina
((37, 15),	(41, 22)),	# Brazil
((27, 50),	(35, 52)),	# Canada
)

dChangedCoreArea = {
iChina : 	((99, 41),	(107, 47)),
iGreece :	((65, 39), 	(69, 42)),
iIndia : 	((88, 33),	(91, 38)),
iPhoenicia:	((54, 37),	(60, 39)),
iMaya : 	((24, 26),	(31, 32)),	# Colombia
iByzantium :	((67, 44),	(69, 46)),
iJapan : 	((111, 41),	(116, 49)),
iArabia : 	((73, 38),	(78, 42)),
iKhmer : 	((97, 35),	(102, 38)),
iMoors : 	((51, 37),	(56, 39)),
iSpain : 	((49, 40),	(55, 46)),
iHolyRome : 	((61, 46),	(66, 51)),
iItaly : 	((58, 40),	(63, 47)),
iMongolia : 	((95, 46),	(106, 52)),
iAztecs : 	((16, 35),	(19, 40)),	# Mexico
iMughals : 	((86, 37),	(94, 43)),
iTurkey : 	((67, 42),	(76, 47)),
iGermany : 	((58, 49),	(63, 55)),
}

dCoreAreaExceptions = {
iChina : [(106, 47)],
iHarappa : [(85, 41), (88, 37), (88, 38)],
iGreece : [(64, 45), (65, 45)],
iPersia : [(85, 37), (85, 38), (85, 39)],
iByzantium : [(71, 40)],
iTibet : [(98, 42)],
iIndonesia : [(100, 30), (101, 29), (101, 30)],
iSpain : [(49, 43), (49, 44), (50, 43), (50, 44)],
iFrance : [(51, 46), (52, 46), (55, 46), (57, 46)],
iHolyRome : [(64, 51), (64, 52), (64, 53), (64, 54)],
iRussia : [(68, 49), (68, 59), (69, 49), (69, 58), (69, 59), (70, 59), (71, 49)],
iPoland : [(63, 50), (64, 50)],
iMongolia : [(102, 47), (103, 47)],
iMughals : [(86, 43)],
iGermany : [(58, 52), (58, 53), (58, 54), (61, 49), (61, 50), (62, 49), (62, 50), (62, 51), (63, 49), (63, 50), (63, 51), (64, 49), (64, 50), (64, 51), (64, 52), (64, 53), (65, 49), (65, 51), (65, 52), (65, 53)],
iAmerica : [(23, 50), (27, 50), (29, 50), (30, 50)],
iArgentina : [(35, 12)],
iCanada : [(29, 50), (30, 50), (31, 50), (32, 50), (32, 51)],
}

dChangedCoreAreaExceptions = {
iChina : [(99, 41), (106, 47)],
iGreece : [(64, 45), (65, 45), (66, 46)],
#iPersia : [], # Iran
iMaya : [(30, 26), (30, 27), (30, 28), (30, 29), (31, 26), (31, 27)], # Colombia
iSpain : [(49, 41), (49, 42), (49, 43), (49, 44), (50, 42), (50, 43), (50, 44), (55, 46)],
iHolyRome : [(61, 51), (64, 51), (65, 51), (66, 51)],
iItaly : [(63, 46), (63, 47)],
iAztecs : [(19, 40)], # Mexico
iMughals : [(92, 43), (93, 43), (94, 42), (94, 43)],
iTurkey : [(67, 42), (70, 42), (71, 42), (73, 42), (74, 42), (75, 42)],
iGermany : [(62, 49), (62, 50), (62, 51), (63, 49), (63, 50), (63, 51)],
}

### Normal Area ###

tNormalArea = (
((65, 30), 	(72, 37)), 	# Egypt
((99, 39), 	(108, 50)), 	# China
((74, 38), 	(79, 44)), 	# Babylonia
((84, 35), 	(88, 42)), 	# Harappa
((64, 39), 	(68, 44)), 	# Greece
((89, 38), 	(96, 42)), 	# India
((72, 39), 	(74, 41)), 	# Carthage
((3, 15), 	(13, 21)), 	# Polynesia
((79, 37), 	(86, 46)), 	# Persia
((57, 40), 	(63, 47)), 	# Rome
((90, 28), 	(93, 34)), 	# Tamils
((68, 25), 	(77, 30)), 	# Ethiopia
((108, 45), 	(110, 49)), 	# Korea
((20, 32), 	(23, 37)), 	# Maya
((64, 40), 	(72, 45)), 	# Byzantium
((111, 41), 	(116, 52)), 	# Japan
((58, 56), 	(67, 65)), 	# Vikings
((72, 30), 	(82, 38)), 	# Arabia
((92, 41), 	(98, 45)), 	# Tibet
((98, 26), 	(103, 37)), 	# Khmer
((98, 24), 	(113, 31)), 	# Indonesia
((51, 37), 	(58, 43)), 	# Moors
((49, 40), 	(55, 46)), 	# Spain
((51, 46), 	(58, 52)), 	# France
((50, 53), 	(54, 60)), 	# England
((58, 48), 	(65, 54)), 	# Holy Rome
((68, 49), 	(83, 62)), 	# Russia
((48, 26), 	(60, 33)), 	# Mali
((63, 50), 	(69, 55)), 	# Poland
((44, 41), 	(50, 44)), 	# Portugal
((24, 14), 	(30, 29)), 	# Inca
((57, 40), 	(63, 47)), 	# Italy
((92, 48), 	(104, 54)), 	# Mongolia
((15, 35), 	(20, 40)), 	# Aztecs
((86, 37), 	(94, 43)), 	# Mughals
((68, 42), 	(78, 49)), 	# Turkey
((99, 31), 	(103, 37)), 	# Thailand
((61, 19), 	(65, 22)), 	# Congo
((56, 51), 	(58, 54)), 	# Holland
((59, 48), 	(66, 55)), 	# Germany
((11, 43), 	(31, 49)), 	# America
((31,  3), 	(36, 15)), 	# Argentina
((32, 14), 	(43, 28)), 	# Brazil
(( 8, 50), 	(37, 67)), 	# Canada
)

dChangedNormalArea = {
iIndia : 	((96, 42),	(97, 42)),
iPhoenicia : 	((71, 39),	(74, 41)),
iMaya : 	((24, 26),	(29, 32)), # Colombia
iArabia : 	((73, 30),	(82, 38)),
iHolyRome : 	((61, 46),	(66, 50)),
}

dNormalAreaExceptions = {
iEgypt : [(72, 37), (70, 30), (71, 30), (72, 30)],
iChina : [(99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50), (100, 39), (101, 39)],
iHarappa : [(84, 41), (84, 42), (84, 43), (85, 41), (85, 42), (85, 43), (86, 43)],
iIndia : [(93, 42), (94, 42), (95, 42), (96, 42)],
iPolynesia : [(13, 21)],
iPersia : [(86, 39), (86, 38), (86, 37)],
iRome : [(62, 47), (63, 47), (63, 46)],
iEthiopia : [(76, 30), (77, 30)],
iJapan : [(111, 52), (112, 52), (111, 51)],
iVikings : [(65, 56), (66, 56), (67, 56), (66, 57), (67, 57)],
iArabia : [(81, 38), (82, 38), (82, 37)],
iSpain : [(49, 44), (49, 43), (49, 42), (49, 41)],
iFrance : [(51, 46), (52, 46), (53, 46), (58, 47), (58, 46), (58, 51), (58, 52), (57, 52)],
iRussia : [(80, 49), (68, 62), (68, 61), (68, 60), (68, 59)],
iPoland : [(63, 50), (64, 50)],
iItaly : [(62, 47), (63, 47), (63, 46)],
iMongolia : [(92, 52), (92, 53), (92, 54), (93, 54), (94, 54), (100, 48), (101, 48), (102, 48), (103, 48), (104, 48)],
iAztecs : [(20, 35)],
iArgentina : [(35, 12), (35, 13), (36, 12), (36, 13), (36, 14), (36, 15)],
iCanada : [(11,50), (12,50), (13,50), (14,50), (16,50), (17,50), (18,50), (19,50), (20,50), (21,50), (22,50), (23,50), (24,50), (25,50), (29,50), (30,50), (31,50), (32,50), (32,51), (8,59), (8,60), (8,61), (8,62), (8,63), (8,64), (8,65), (9,59), (9,60), (9,61), (9,62), (9,63), (9,64), (9,65), (37,66), (37,67)],
}

dChangedNormalAreaExceptions = {
iChina : [(99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50)],
}

### Broader Area ###

tBroaderArea = (
((60, 26), 	(74, 38)), 	# Egypt
((95, 38), 	(108, 50)), 	# China
((72, 37), 	(78, 44)), 	# Babylonia
((90, 40), 	(90, 40)), 	# Harappa
((62, 39), 	(77, 47)), 	# Greece
((85, 28), 	(99, 43)), 	# India
((71, 39), 	(74, 41)), 	# Carthage
((1, 15), 	(17, 38)), 	# Polynesia
((70, 37), 	(87, 49)), 	# Persia
((49, 35), 	(73, 50)), 	# Rome
((90, 28), 	(93, 34)), 	# Tamils
((67, 21), 	(77, 30)), 	# Ethiopia
((106, 45), 	(110, 52)), 	# Korea
((19, 30), 	(26, 37)), 	# Maya
((58, 34), 	(74, 45)), 	# Byzantium
((110, 40), 	(116, 56)), 	# Japan
((58, 56), 	(71, 65)), 	# Vikings
((64, 30), 	(85, 44)), 	# Arabia
((92, 41), 	(98, 45)), 	# Tibet
((97, 25), 	(105, 39)), 	# Khmer
((98, 24), 	(113, 31)), 	# Indonesia
((51, 37), 	(58, 43)), 	# Moors
((49, 38), 	(55, 46)), 	# Spain
((49, 44), 	(61, 52)), 	# France
((48, 53), 	(54, 60)), 	# England
((58, 43), 	(64, 54)), 	# Holy Rome
((65, 48), 	(92, 59)), 	# Russia
((48, 21), 	(67, 32)), 	# Mali
((63, 50), 	(67, 55)), 	# Poland
((49, 40), 	(51, 45)), 	# Portugal
((24, 14), 	(30, 27)), 	# Inca
((57, 47), 	(65, 47)), 	# Italy
((82, 44), 	(110, 62)), 	# Mongolia
((14, 32), 	(24, 43)), 	# Aztecs
((86, 37), 	(94, 43)), 	# Mughals
((68, 42), 	(86, 49)), 	# Turkey
((97, 25), 	(105, 39)), 	# Thailand
((61, 19), 	(65, 22)), 	# Congo
((56, 51), 	(58, 54)), 	# Holland
((55, 46), 	(67, 57)), 	# Germany
((10, 42), 	(37, 56)), 	# America
((29,  3), 	(36, 15)), 	# Argentina
((32, 14), 	(43, 28)), 	# Brazil
(( 8, 50), 	(37, 67)), 	# Canada
)

dChangedBroaderArea = {
iMaya :		((33, 32),	(33, 32)),	# Colombia
iByzantium : 	((64, 38),	(74, 45)),
iHolyRome :	((61, 46),	(66, 50)),
iMughals :	((84, 37),	(94, 43)),
}

### Respawn area ###

dRespawnArea = {
iEgypt :	((65, 30),	(71, 39)),
iChina :	((99, 39),	(107, 47)),
iIndia :	((88, 33),	(96, 41)),
iByzantium :	((65, 40),	(69, 46)),
iMoors :	((48, 34),	(58, 39)),
iInca :		((25, 16),	(33, 25)),
iMughals :	((85, 37),	(88, 43)),
}

### Rebirth area ###

dRebirthPlot = {
iPersia : (81, 41),	# Esfahan (Iran)
iMaya : (27, 29),	# Bogota (Colombia)
iAztecs : (18, 37),	# Mexico City (Mexico)
}

dRebirthArea = {
iPersia :	((78, 38),	(86, 43)),	# Iran
iMaya :		((23, 25), 	(31, 32)),	# Colombia
iAztecs :	((11, 34), 	(23, 48)),	# Mexico
}

dRebirthAreaExceptions = {
iAztecs : [(17, 48), (18, 48), (19, 48), (20, 48), (21, 48), (22, 48), (23, 48), (18, 47), (19, 47), (20, 47), (21, 47), (22, 47), (23, 47), (18, 46), (19, 46), (20, 46), (21, 46), (22, 46), (23, 46), (21, 45), (22, 45), (23, 45), (22, 44), (23, 44), (22, 43), (23, 43), (23, 42), (22, 35), (21, 34), (22, 34), (23, 34)],
}