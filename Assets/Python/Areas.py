from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = [(33, 12), (35, 23), (32, 25), (28, 29), (104, 56)]

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
	if iPlayer in dChangedBirthArea and bExtended:
		return dChangedBirthArea[iPlayer]
	return tBirthArea[iPlayer]
	
def getBirthExceptions(iPlayer):
	if iPlayer in dBirthAreaExceptions: return dBirthAreaExceptions[iPlayer]
	return []
	
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
	x, y = tPlot
	plot = gc.getMap().plot(x, y)
	for iLoopPlayer in range(iNumPlayers):
		if iLoopPlayer == iPlayer: continue
		if plot.isCore(iLoopPlayer):
			return True
	return False
	
def isExtendedBirth(iPlayer):
	if gc.getGame().getActivePlayer() == iPlayer: return False
	
	# add special conditions for extended AI flip zones here
	if iPlayer == iOttomans and pByzantium.isAlive(): return False
	
	return True
			
def init():
	for iPlayer in range(iNumPlayers):
		updateCore(iPlayer)
	
### Capitals ###

tCapitals = (
(79, 43), # Memphis
(89, 47), # Babylon
(101, 47), # Harappa
(121, 52), # Chang'an
(77, 51), # Athens
(110, 44), # Pataliputra
(84, 47), # Sur
(3, 20), # Tonga
(94, 44), # Persepolis
(69, 54), # Rome
(22, 41), # Tikal
(106, 33), # Thanjavur
(84, 35), # Aksum
(131, 54), # Seoul
(80, 55), # Constantinople
(136, 53), # Kyoto
(68, 71), # Oslo
(0, 0), # Leoreth: to do new map
(86, 39), # Mecca
(113, 48), # Lhasa
(121, 27), # Palembang
(58, 49), # Cordoba
(59, 52), # Madrid
(62, 60), # Paris
(121, 37), # Angkor
(59, 63), # London
(66, 62), # Cologne
(85, 65), # Moskow
(60, 37), # Timbuktu
(75, 62), # Krakow
(55, 51), # Lisboa
(31, 24), # Cuzco
(67, 57), # Mailand
(118, 62), # Karakorum
(17, 43), # Tenochtitlan
(105, 46), # Delhi
(81, 54), # Sogut
(119, 37), # Ayutthaya
(70, 25), # Mbanza Kongo
(64, 64), # Amsterdam
(70, 64), # Berlin
(29, 54), # Washington
(38, 13), # Buenos Aires
(46, 21), # Rio de Janeiro
(30, 60), # Ottawa
)

dChangedCapitals = {
iChina : (124, 56),	# Beijing
iIndia : (105, 46),	# Delhi
iCarthage : (68, 48),	# Carthage
iPersia : (93, 47),	# Esfahan (Iran)
iTamils : (105, 36),	# Vijayanagara
iMaya : (29, 34),	# Bogota (Colombia)
iKhmer : (122, 42),	# Hanoi
iHolyRome : (72, 59),	# Vienna
}

# new capital locations if changed during the game
dNewCapitals = {
iJapan : (139, 54),	# Tokyo
iVikings : (73, 70),	# Stockholm
iHolyRome : (72, 59),	# Vienna
iItaly : (69, 54),	# Rome
iMongolia : (124, 56),	# Khanbaliq
iOttomans : (80, 55),	# Istanbul
}

# new capital locations on respawn
dRespawnCapitals = {
iEgypt : (80, 43),	# Cairo
iChina :  (124, 56),	# Beijing
iIndia : (105, 46),	# Delhi
iPersia : (93, 47),	# Esfahan
iEthiopia : (84, 32),	# Addis Ababa
iJapan : (139, 54),	# Tokyo
iVikings : (73, 70),	# Stockholm
iTurks: (0, 0), # Herat # Leoreth: to do new map
iIndonesia : (124, 25),	# Jakarta
iMoors : (58, 44),	# Marrakesh
iHolyRome : (72, 59),	# Vienna
iInca : (28, 25),	# Lima
iItaly : (69, 54),	# Rome
iMughals : (99, 43),	# Karachi
iOttomans : (80, 55),	# Istanbul
}

### Birth Area ###

tBirthArea = (
((77, 37),	(81, 44)),	# Egypt
((88, 44),	(91, 48)),	# Babylonia
((99, 45),	(103, 49)),	# Harappa
((120, 50),	(129, 56)), # China
((75, 49),	(81, 55)),	# Greece
((101, 42),	(114, 48)),	# India
((83, 47),	(86, 49)),	# Carthage
((2, 19),	(5, 25)),	# Polynesia
((91, 43),	(98, 52)),	# Persia
((66, 50),	(73, 57)),	# Rome
((20, 41),	(23, 44)),	# Maya
((105, 30),	(109, 36)),	# Tamils
((82, 32),	(86, 36)),	# Ethiopia
((129, 53),	(132, 57)),	# Korea
((75, 45),	(86, 57)),	# Byzantium
((133, 49),	(139, 59)),	# Japan
((65, 67),	(73, 73)),	# Vikings
((0, 0), (0, 0)),				# Turks # Leoreth: to do new map
((78, 35),	(91, 48)),	# Arabia
((107, 47),	(115, 54)),	# Tibet
((116, 25),	(128, 33)),	# Indonesia
((57, 43),	(68, 51)),	# Moors
((55, 51),	(60, 54)),	# Spain
((57, 55),	(65, 61)),	# France
((118, 34),	(123, 38)),	# Khmer
((56, 62),	(60, 70)),	# England
((63, 58),	(73, 65)),	# Holy Rome
((81, 61),	(89, 69)),	# Russia
((54, 31),	(65, 38)),	# Mali
((73, 60),	(79, 66)),	# Poland
((49, 49),	(56, 52)),	# Portugal
((28, 23),	(32, 24)),	# Inca
((66, 55),	(71, 57)),	# Italy
((105, 53),	(130, 65)),	# Mongolia
((13, 41),	(19, 47)),	# Aztecs
((99, 44),	(106, 50)),	# Mughals
((80, 49),	(87, 55)),	# Ottomans
((118, 34), (120, 41)),	# Thailand
((69, 24),	(74, 27)),	# Congo
((63, 62),	(65, 65)),	# Netherlands
((65, 62),	(75, 66)),	# Germany
((24, 50),	(33, 59)),	# America
((38, 3),	(39, 17)),	# Argentina
((40, 16),	(49, 32)),	# Brazil
((18, 59),	(37, 71)),	# Canada
)

dChangedBirthArea = {
iPersia :	((86, 43),	(98, 54)),	# includes Assyria and Anatolia
iSpain : 	((55, 51),	(64, 54)),	# includes Catalonia
iInca : 	((27, 21),	(35, 26)),
iMongolia : 	((81, 45),	(105, 54)),	# 6 more west, 1 more south
iOttomans : 	((79, 49), 	(87, 56)), 	# includes Constantinople
iArgentina : 	((29, 3),	(35, 13)),	# includes Chile
}

dBirthAreaExceptions = {
iChina : [(120, 50), (120, 56), (121, 56), (122, 56), (121, 55), (122, 55), (120, 54), (128, 56)],
iBabylonia : [(91, 47), (91, 48)],
iHarappa : [(99, 49), (102, 45), (103, 45)],
iGreece : [(75, 54), (75, 55), (76, 55), (77, 55)],
iIndia : [(111, 48), (112, 47), (113, 47), (113, 48), (114, 48)],
iRome : [(67, 51), (67, 52), (72, 56), (72, 57), (73, 55), (73, 56), (73, 57)],
iByzantium : [(75, 45), (76, 45)],
iTurks : [], # Leoreth: to do new map
iArabia : [(82, 34), (91, 47), (78, 35), (79, 35), (80, 35), (81, 35), (82, 35), (83, 35), (84, 35), (85, 35), (78, 36), (79, 36), (80, 36), (81, 36), (82, 36), (83, 36), (84, 36), (78, 37), (79, 37), (80, 37), (81, 37), (82, 37), (83, 37), (84, 37), (78, 38), (79, 38), (80, 38), (81, 38), (82, 38), (83, 38), (83, 39)],
iTibet : [(107, 47), (108, 47), (107, 53), (108, 53), (107, 54), (108, 54), (109, 54), (110, 54)],
iIndonesia : [(100, 31), (100, 30), (101, 29), (101, 30)],
iMoors : [(64, 51), (67, 51)],
iSpain : [(55, 51), (56, 51), (55, 52), (56, 52)],
iFrance : [(65, 60), (65, 61)],
iHolyRome : [(63, 58), (63, 59), (63, 60), (63, 61), (63, 62), (64, 58), (64, 59), (64, 60), (64, 61), (64, 62), (65, 58), (65, 59), (72, 63), (72, 64), (72, 65), (73, 62), (73, 63), (73, 64), (73, 65)],
iRussia : [(87, 69), (88, 68), (88, 69), (89, 68), (89, 69)],
iPoland : [(73, 60), (73, 61), (75, 60)],
iMongolia : [(112, 53), (113, 54), (114, 53), (114, 54), (115, 53), (120, 53), (121, 53), (121, 54), (122, 53), (122, 54), (123, 53), (123, 54), (123, 55), (123, 56), (124, 53), (124, 54), (124, 55), (124, 56), (125, 53), (125, 54), (125, 55), (125, 56), (126, 53), (126, 54), (126, 56), (127, 53), (128, 54), (130, 55), (130, 56), (130, 57)],
iMughals : [(99, 40), (100, 40), (101, 40), (99, 49), (100, 50)],
iOttomans : [(80, 55), (83, 49), (87, 49), (87, 50), (87, 51)],
iNetherlands : [(65, 62)],
iGermany : [(65, 64), (65, 65), (69, 62), (70, 62), (71, 62), (72, 62), (73, 62), (74, 62), (74, 63), (74, 64), (75, 62), (75, 63), (75, 64)],
iAmerica : [(24, 54), (24, 55), (24, 56), (24, 57), (24, 58), (24, 59), (26, 59), (27, 59), (30, 59), (31, 59)],
iArgentina : [(39, 5), (39, 14), (39, 15)],
iBrazil : [(36, 15), (36, 16)],
iCanada : [(18, 59), (18, 60), (18, 61), (19, 59), (19, 60), (19, 61), (20, 59), (20, 60), (20, 61), (21, 59), (21, 60), (21, 61), (22, 59), (22, 60), (23, 60), (24, 59), (24, 60), (30, 59), (31, 59), (32, 59), (33, 59), (33, 60), (34, 60), (34, 67), (34, 68), (34, 69), (35, 66), (35, 67), (36, 65), (36, 66), (36, 67), (37, 65), (37, 66)],
}

### Core Area ###

tCoreArea = (
((78, 39),	(81, 44)),	# Egypt
((88, 44),	(91, 48)),	# Babylonia
((99, 45),	(103, 49)),	# Harappa
((120, 50),	(129, 56)),	# China
((75, 49),	(81, 55)),	# Greece
((105, 42),	(113, 47)),	# India
((84, 47),	(86, 4)),	# Phoenicia
((3, 20),	(4, 24)),	# Polynesia
((91, 43),	(98, 52)),	# Persia
((66, 50),	(73, 57)),	# Rome
((20, 41),	(23, 44)),	# Maya
((105, 30),	(109, 36)),	# Tamils
((82, 32),	(86, 36)),	# Ethiopia
((130, 53),	(132, 57)),	# Korea
((75, 49),	(84, 56)),	# Byzantium
((135, 52),	(139, 55)),	# Japan
((65, 67),	(73, 73)),	# Vikings
((0, 0), (0, 0)),				# Turks # Leoreth: to do new map
((84, 35),	(89, 46)),	# Arabia
((107, 47),	(115, 54)),	# Tibet
((116, 25),	(127, 29)),	# Indonesia
((57, 43),	(59, 50)),	# Moors
((55, 51),	(60, 54)),	# Spain
((57, 55),	(65, 61)),	# France
((121, 35),	(122, 38)),	# Khmer
((56, 62),	(60, 70)),	# England
((65, 58),	(73, 62)),	# HolyRome
((81, 61),	(89, 69)),	# Russia
((57, 34),	(65, 38)),	# Mali
((73, 60),	(79, 66)),	# Poland
((55, 49),	(56, 52)),	# Portugal
((28, 22),	(32, 25)),	# Inca
((66, 55),	(71, 57)),	# Italy
((113, 56),	(129, 63)),	# Mongolia
((16, 42),	(18, 44)),	# Aztecs
((99, 44),	(106, 50)),	# Mughals
((80, 49),	(87, 55)),	# Turkey
((118, 36),	(120, 38)),	# Thailand
((69, 24),	(74, 27)),	# Congo
((63, 62),	(65, 65)),	# Netherlands
((65, 59),	(75, 66)),	# Germany
((22, 53),	(33, 59)),	# America
((35, 9),	(39, 17)),	# Argentina
((41, 19),	(48, 27)),	# Brazil
((26, 59),	(37, 63)),	# Canada
)

dChangedCoreArea = {
iChina :	((120, 47),	(129, 56)),
iGreece :	((75, 49),	(79, 52)),
iIndia :	((103, 37),	(106, 41)),
iPhoenicia :	((63, 45),	(70, 48)),
iMaya :	((26, 30),	(35, 38)),	# Colombia
iByzantium :	((79, 54),	(81, 56)),
iJapan :	((133, 49), (139, 59)),
iTurks :	((0, 0), (0, 0)),	# Leoreth: to do new map
iArabia :	((83, 44),	(91, 48)),
iMoors :	((57, 43),	(66, 48)),
iSpain :	((55, 48),	(64, 54)),
iKhmer :	((121, 37),	(124, 43)),
iHolyRome :	((69, 58),	(76, 62)),
iItaly :	((66, 49),	(73, 57)),
iMongolia :	((114, 53),	(129, 59)),
iAztecs :	((14, 41),	(21, 47)),	# Mexico
iMughals :	((99, 44),	(108, 50)),
iOttomans :	((79, 49),	(87, 56)),
iGermany :	((65, 59),	(71, 66)),
}

dCoreAreaExceptions = {
iChina : [(120, 50), (120, 56), (121, 56), (122, 56), (121, 55), (122, 55), (120, 54), (128, 56)],
iBabylonia : [(91, 47), (91, 48)],
iHarappa : [(99, 49), (102, 45), (103, 45)],
iGreece : [(75, 54), (75, 55), (76, 55), (77, 55)],
iIndia : [(105, 42), (106, 42), (107, 42), (112, 47), (113, 47)],
iRome : [(67, 51), (67, 52), (72, 56), (72, 57), (73, 55), (73, 56), (73, 57)],
iByzantium : [(83, 49), (75, 55), (76, 55), (75, 56), (76, 56), (77, 56), (78, 56)],
iTurks : [], # Leoreth: to do new map
iArabia : [(84, 35), (85, 35), (84, 36), (84, 37), (88, 45), (88, 46), (89, 45), (89, 46)],
iTibet : [(107, 47), (108, 47), (107, 53), (108, 53), (107, 54), (108, 54), (109, 54), (110, 54)],
iIndonesia : [(120, 30), (124, 30), (125, 30), (127, 30)],
iSpain : [(55, 51), (56, 51), (55, 52), (56, 52)],
iFrance : [(65, 60), (65, 61)],
iHolyRome : [(65, 58), (65, 59), (73, 62)],
iRussia : [(81, 61), (81, 62), (81, 63), (82, 61), (82, 62), (82, 63), (83, 61), (83, 62), (83, 63), (84, 61), (84, 62), (85, 61), (85, 62), (86, 61), (87, 69), (88, 68), (88, 69), (89, 68), (89, 69)],
iPoland : [(73, 60), (73, 61), (75, 60)],
iMongolia : [(123, 56), (123, 63), (124, 56), (124, 63), (125, 56), (125, 62), (126, 56), (126, 62), (126, 63), (127, 61), (127, 63), (128, 61), (128, 62), (128, 63), (129, 60), (129, 61), (129, 62), (129, 63)],
iMughals : [(99, 40), (100, 40), (101, 40), (99, 49), (100, 50)],
iOttomans : [(80, 55), (83, 49), (87, 49), (87, 50), (87, 51)],
iNetherlands : [(65, 62)],
iGermany : [(65, 59), (65, 60), (65, 64), (65, 65), (69, 61), (69, 62), (70, 59), (70, 60), (70, 61), (70, 62), (71, 59), (71, 60), (71, 61), (71, 62), (72, 59), (72, 60), (72, 61), (72, 62), (73, 59), (73, 60), (73, 61), (73, 62), (74, 59), (74, 61), (74, 62), (74, 63), (74, 64), (75, 59), (75, 60), (75, 61), (75, 62), (75, 63), (75, 64)],
iAmerica : [(22, 53), (22, 54), (22, 55), (22, 56), (22, 59), (23, 53), (23, 54), (23, 55), (24, 53), (24, 54), (25, 53), (26, 59), (27, 59), (30, 59), (31, 59)],
iArgentina : [(39, 14), (39, 15)],
iCanada : [(26, 63), (27, 63), (28, 63), (29, 63), (30, 59), (31, 59), (32, 59), (33, 59), (33, 60), (34, 60)],
}

dChangedCoreAreaExceptions = {
iChina : [(120, 56), (121, 56), (122, 56), (121, 55), (122, 55), (120, 54), (128, 56), (120, 47), (120, 48), (120, 49), (120, 50)],
iIndia : [(105, 37), (106, 37), (106, 38)],
iMaya : [(31, 30), (32, 30), (33, 30), (34, 30), (35, 30), (32, 31), (33, 31), (34, 31), (35, 31), (32, 32), (33, 32), (34, 32), (35, 32), (32, 33), (33, 33), (34, 33)], # Colombia
iArabia : [(82, 34), (91, 47)],
iKhmer:	[(121, 37), (122, 37), (121, 38), (124, 41), (124, 43)],
iMoors : [(58, 48)],
iSpain : [(56, 49), (55, 50), (56, 50), (55, 51), (56, 51), (55, 52), (56, 52), (63, 48), (64, 48)],
iHolyRome : [(69, 59), (69, 60), (73, 62), (74, 61), (74, 62), (75, 61), (75, 62), (76, 61), (76, 62)],
iItaly : [(72, 56), (72, 57), (73, 55), (73, 56), (73, 57)],
iMongolia : [(114, 53), (114, 54), (115, 53), (120, 53), (121, 53), (122, 53), (123, 53), (124, 53), (125, 53), (126, 53), (127, 53), (128, 54)],
iMughals : [(99, 40), (100, 40), (101, 40), (99, 49), (100, 50), (107, 50), (108, 50)],
iOttomans : [(79, 49), (80, 55), (83, 49), (87, 49), (87, 50), (87, 51)],
iGermany : [(65, 59), (65, 64), (65, 65), (69, 61), (69, 62), (70, 59), (70, 60), (70, 61), (70, 62), (71, 59), (71, 60), (71, 61), (71, 62)],
}

### Normal Area ###

tNormalArea = (
((75, 37),	(82, 45)),	# Egypt
((87, 44),	(91, 51)),	# Babylonia
((98, 42),	(103, 50)), # Harappa
((117, 43),	(130, 59)),	# China
((75, 49),	(79, 54)),	# Greece
((104, 42),	(114, 48)),	# India
((83, 46),	(86, 49)),	# Carthage
((3, 20),	(11, 24)),	# Polynesia
((91, 43),	(100, 54)),	# Persia
((64, 49),	(74, 59)),	# Rome
((20, 37),	(25, 44)),	# Maya
((105, 30),	(109, 38)),	# Tamils
((81, 29),	(90, 36)),	# Ethiopia
((130, 53),	(132, 57)),	# Korea
((75, 49),	(84, 56)),	# Byzantium
((133, 49),	(139, 62)),	# Japan
((65, 67),	(79, 77)),	# Vikings
((0, 0), (0, 0)),				# Turks # Leoreth: to do new map
((84, 35),	(96, 46)),	# Arabia
((107, 47),	(115, 54)),	# Tibet
((116, 25),	(136, 33)),	# Indonesia
((57, 43),	(68, 51)),	# Moors
((55, 48),	(64, 54)),	# Spain
((57, 55),	(65, 61)),	# France
((118, 34),	(123, 41)),	# Khmer
((56, 62),	(60, 70)),	# England
((65, 58),	(73, 62)),	# HolyRome
((80, 58),	(100, 77)),	# Russia
((54, 31),	(68, 38)),	# Mali
((73, 60),	(82, 66)),	# Poland
((49, 49),	(56, 52)),	# Portugal
((26, 13),	(34, 34)),	# Inca
((66, 49),	(73, 57)),	# Italy
((113, 56),	(129, 66)),	# Mongolia
((12, 41),	(21, 47)),	# Aztecs
((99, 44),	(108, 50)),	# Mughals
((79, 49),	(91, 59)),	# Ottomans
((118, 34),	(122, 41)),	# Thailand
((69, 24),	(74, 27)),	# Congo
((63, 62),	(65, 65)),	# Netherlands
((65, 58),	(75, 66)),	# Germany
((8, 49),	(33, 59)),	# America
((34, 3),	(39, 17)),	# Argentina
((36, 16),	(49, 36)),	# Brazil
((7, 59),	(40, 79)),	# Canada
)

dChangedNormalArea = {
iIndia : 	((96, 42),	(97, 42)),
iCarthage :	((63, 45),	(70, 48)),
iMaya : 	((26, 30),	(35, 38)),	# Colombia
iArabia : 	((84, 35),	(91, 48)),
iKhmer : 	((121, 35),	(124, 43)),
iHolyRome : ((69, 56),	(78, 62)),
}

dNormalAreaExceptions = {
iChina : [(117, 43), (117, 44), (117, 45), (118, 43), (119, 43), (120, 43), (121, 43), (122, 43), (123, 43), (130, 55), (130, 56), (130, 57), (130, 58), (130, 59), (117, 59), (118, 59), (119, 59), (120, 59)],
iBabylonia : [(90, 50), (90, 51), (91, 50), (91, 51)],
iHarappa : [(98, 47), (98, 48), (99, 49), (102, 42), (102, 43), (102, 44), (103, 42), (103, 43), (103, 44), (103, 45)],
iGreece : [(75, 54)],
iIndia : [(105, 42), (106, 42), (107, 42), (112, 47), (113, 47)],
iPolynesia : [(10, 24)],
iPersia : [(91, 53), (91, 54), (99, 43), (99, 44), (99, 45), (99, 46), (100, 43), (100, 44), (100, 45), (100, 46), (100, 47), (100, 48)],
iRome : [(64, 51), (64, 57), (74, 57)],
iEthiopia : [(81, 34), (81, 35), (81, 36), (88, 35), (88, 36), (89, 35), (90, 36)],
iByzantium : [(83, 49), (75, 55), (76, 55), (75, 56), (76, 56), (77, 56), (78, 56)],
iJapan : [(133, 60), (134, 60), (133, 61), (134, 61), (133, 62), (134, 62)],
iVikings : [(75, 67), (77, 67), (78, 67), (77, 68), (78, 68), (79, 68)],
iTurks : [], # Leoreth: to do new map
iArabia : [(84, 35), (84, 36), (84, 37), (85, 35), (88, 45), (88, 46), (89, 45), (89, 46), (90, 44), (90, 45), (90, 46), (91, 45), (91, 46), (92, 45), (92, 46), (93, 44), (93, 45), (94, 43), (94, 44), (94, 45), (94, 46), (95, 43), (95, 45), (95, 46), (96, 43), (96, 44), (96, 45), (96, 46)],iSpain : [(49, 44), (49, 43), (49, 42), (49, 41)],
iTibet : [(107, 47), (108, 47), (107, 53), (108, 53), (107, 54), (108, 54), (109, 54), (110, 54)],
iIndonesia : [(131, 33)],
iMoors : [(64, 51), (67, 51)],
iSpain : [(63, 48), (64, 48)],
iFrance : [(65, 60), (65, 61)],
iKhmer:	[(121, 41), (122, 40), (123, 39)],
iHolyRome : [(65, 58), (65, 59), (73, 62)],
iRussia : [(80, 58), (80, 59), (93, 58), (93, 60), (93, 61), (94, 58), (94, 59), (94, 60), (94, 61), (94, 77), (95, 58), (95, 60), (95, 61), (95, 76), (95, 77), (96, 60), (96, 61), (96, 76), (97, 60), (97, 61), (97, 62), (98, 58), (98, 59), (98, 60), (98, 61), (98, 62), (99, 58), (99, 59), (99, 60), (99, 61), (99, 62), (99, 63), (100, 58), (100, 59), (100, 60), (100, 61), (100, 62), (100, 63), (100, 64), (100, 65)],
iPoland : [(73, 60), (73, 61), (75, 60), (81, 66), (82, 66)],
iInca : [(28, 29), (30, 27), (30, 28), (30, 29), (30, 30), (30, 31), (31, 27), (31, 28), (31, 29), (31, 30), (31, 31), (31, 32), (31, 33), (32, 25), (32, 27), (32, 28), (32, 29), (32, 30), (32, 31), (32, 32), (32, 33), (32, 34), (33, 26), (33, 27), (33, 28), (33, 29), (33, 30), (33, 31), (33, 32), (33, 33), (33, 34), (34, 25), (34, 26), (34, 27), (34, 28), (34, 29), (34, 30), (34, 31), (34, 32), (34, 33)],
iItaly : [(72, 56), (72, 57), (73, 55), (73, 56), (73, 57)],
iMongolia : [(113, 65), (113, 66), (114, 66), (118, 56), (119, 56), (119, 57), (120, 56), (120, 57), (120, 58), (121, 56), (121, 57), (121, 58), (122, 56), (122, 57), (123, 56), (123, 57), (123, 66), (124, 56), (124, 57), (124, 63), (124, 64), (124, 65), (124, 66), (125, 56), (125, 57), (125, 62), (125, 64), (125, 65), (125, 66), (126, 56), (126, 62), (126, 63), (126, 64), (126, 65), (126, 66), (127, 61), (127, 63), (127, 64), (127, 65), (127, 66), (128, 61), (128, 62), (128, 63), (128, 64), (128, 65), (128, 66), (129, 60), (129, 61), (129, 62), (129, 63), (129, 64), (129, 65), (129, 66)],
iMughals : [(99, 40), (100, 40), (101, 40), (99, 49), (100, 50), (107, 50), (108, 50)],
iOttomans : [(79, 49), (80, 55), (83, 49), (87, 49), (87, 50), (87, 51), (88, 49), (88, 50), (88, 51), (89, 49), (89, 50), (89, 51), (90, 49), (90, 50), (90, 51), (91, 50), (91, 51)],
iThailand : [(122, 39), (122, 40), (121, 40), (121, 41)],
iNetherlands : [(65, 62)],
iGermany : [(65, 58), (65, 59), (65, 64), (65, 65), (74, 58), (74, 59), (74, 61), (74, 62), (74, 63), (74, 64), (75, 58), (75, 59), (75, 60), (75, 61), (75, 62), (75, 63), (75, 64)],
iAmerica : [(10, 49), (12, 49), (13, 49), (14, 49), (15, 49), (26, 49), (26, 59), (27, 59), (30, 59), (31, 59)],
iArgentina : [(39, 5), (39, 14), (39, 15)],
iBrazil : [(36, 17), (36, 18), (36, 19), (36, 20), (36, 21), (36, 22), (36, 23), (36, 24), (36, 25), (36, 36), (37, 16), (37, 17), (37, 18), (37, 19), (37, 20), (37, 21), (37, 22), (37, 23), (37, 24), (38, 16), (38, 17), (38, 18), (38, 19), (38, 20), (38, 21), (38, 22), (38, 23), (39, 16), (39, 17), (39, 18), (39, 19)],
iCanada : [(8, 59), (8, 60), (9, 60), (9, 61), (10, 59), (10, 60), (11, 59), (12, 60), (12, 61), (13, 59), (14, 59), (14, 60), (14, 61), (15, 59), (15, 60), (15, 61), (16, 59), (16, 60), (16, 61), (17, 59), (17, 60), (17, 61), (18, 59), (18, 60), (18, 61), (19, 59), (19, 60), (19, 61), (20, 59), (20, 60), (20, 61), (21, 59), (21, 60), (21, 61), (22, 59), (22, 60), (23, 60), (24, 59), (24, 60), (30, 59), (31, 59), (32, 59), (33, 59), (33, 60), (34, 60), (39, 78), (40, 74), (40, 76)],
}

dChangedNormalAreaExceptions = {
iMaya : [(31, 30), (32, 30), (33, 30), (34, 30), (35, 30), (32, 31), (33, 31), (34, 31), (35, 31), (32, 32), (33, 32), (34, 32), (35, 32), (32, 33), (33, 33), (34, 33)], # Colombia
iArabia : [(84, 35), (84, 36), (84, 37), (85, 35), (91, 47), (91, 48)],
iKhmer:	[(121, 35), (122, 35), (121, 36), (122, 36), (121, 37), (122, 37), (121, 38), (124, 41), (124, 43)],
iHolyRome : [(69, 59), (69, 60), (73, 62), (74, 62), (75, 56), (75, 57), (75, 62), (76, 56), (76, 57), (76, 62), (77, 56), (77, 57), (77, 62), (78, 56), (78, 57), (78, 62)],
}

### Broader Area ###

tBroaderArea = (
((70, 32),	(85, 46)),	# Egypt
((83, 44),	(91, 52)),	# Babylonia
((97, 42),	(104, 51)),	# Harappa
((111, 41),	(130, 59)),	# China
((71, 46),	(90, 55)),	# Greece
((99, 30),	(114, 51)),	# India
((83, 46),	(86, 49)),	# Carthage
((0, 17),	(20, 35)),	# Polynesia
((82, 43),	(106, 59)),	# Persia
((55, 43),	(85, 59)),	# Rome
((19, 36),	(27, 44)),	# Maya
((104, 26),	(121, 38)),	# Tamils
((79, 24),	(90, 37)),	# Ethiopia
((128, 53),	(133, 61)),	# Korea
((67, 42),	(86, 56)),	# Byzantium
((133, 46),	(139, 67)),	# Japan
((65, 66),	(86, 77)),	# Vikings
((0, 0), (0, 0)),				# Turks # Leoreth: to do new map
((74, 35),	(98, 54)),	# Arabia
((107, 47),	(115, 54)),	# Tibet
((116, 25),	(136, 33)),	# Indonesia
((57, 43),	(68, 51)),	# Moors
((55, 45),	(66, 54)),	# Spain
((55, 53),	(70, 64)),	# France
((115, 34),	(124, 43)),	# Khmer
((53, 62),	(60, 70)),	# England
((63, 54),	(73, 65)),	# Holy Rome
((75, 57),	(110, 77)),	# Russia
((54, 31),	(68, 38)),	# Mali
((73, 60),	(82, 66)),	# Poland
((49, 48),	(58, 52)),	# Portugal
((26, 13),	(34, 34)),	# Inca
((66, 49),	(74, 57)),	# Italy
((86, 52),	(132, 68)),	# Mongolia
((12, 37),	(25, 50)),	# Aztecs
((99, 42),	(111, 51)),	# Mughals
((75, 49),	(104, 59)),	# Ottomans
((115, 26),	(122, 44)),	# Thailand
((69, 24),	(74, 27)),	# Congo
((63, 62),	(65, 65)),	# Netherlands
((61, 58),	(77, 68)),	# Germany
((7, 47),	(40, 64)),	# America
((32, 3),	(41, 17)),	# Argentina
((33, 15),	(49, 32)),	# Brazil
((7, 59),	(40, 79)),	# Canada
)

dChangedBroaderArea = {
iCarthage :	((57, 43),	(73, 54)), 	# Carthage
iMaya :		((26, 27),	(38, 38)),	# Colombia
iByzantium :	((64, 38),	(74, 45)),
iHolyRome :	((66, 54),	(79, 62)),
iMughals :	((84, 37),	(94, 43)),
}

### Respawn area ###

dRespawnArea = {
iEgypt :	((75, 37), 	(82, 45)),
iChina :	((117, 46),	(129, 56)),
iIndia :	((103, 37),	(113, 47)),
iByzantium :	((75, 49),	(81, 57)),
iMoors :	((56, 42),	(68, 48)),
iInca :		((26, 17),	(38, 29)),
iMughals :	((85, 37),	(88, 43)),
}

dRespawnAreaExceptions = {
iIndia : [(112, 47), (113, 47)],
iMoors : [(58, 48)],
iInca : [(33, 27), (33, 28), (33, 29), (34, 27), (34, 28), (34, 29), (35, 27), (35, 28), (35, 29), (36, 17), (36, 18), (36, 19), (36, 26), (36, 27), (36, 28), (36, 29), (37, 17), (37, 18), (37, 19), (37, 25), (37, 26), (37, 27), (37, 28), (37, 29), (38, 17), (38, 18), (38, 19), (38, 24), (38, 25), (38, 26), (38, 27), (38, 28), (38, 29)],
}

### Rebirth area ###

dRebirthPlot = {
iPersia : (93, 47),	# Esfahan (Iran)
iMaya : (29, 34),	# Bogota (Colombia)
iAztecs : (17, 43),	# Mexico City (Mexico)
}

dRebirthArea = {
iPersia :	((90, 43),	(98, 53)),	# Iran
iMaya :		((26, 30),	(35, 38)),	# Colombia
iAztecs :	((8, 41),	(23, 55)),	# Mexico
}

dRebirthAreaExceptions = {
iPersia : [(90, 43), (90, 44), (90, 45), (90, 46), (90, 47), (90, 48), (90, 49)],
iMaya :	  [(31, 30), (32, 30), (33, 30), (34, 30), (35, 30), (32, 31), (33, 31), (34, 31), (35, 31), (32, 32), (33, 32), (34, 32), (35, 32), (32, 33), (33, 33), (34, 33)], # Colombia
iAztecs : [(16, 55), (17, 55), (18, 55), (19, 55), (20, 55), (21, 55), (22, 55), (23, 55), (16, 56), (17, 56), (18, 56), (19, 56), (20, 56), (21, 56), (22, 56), (23, 56), (16, 57), (17, 57), (18, 57), (19, 57), (20, 57), (21, 57), (22, 57), (23, 57), (20, 58), (21, 58), (22, 58), (23, 58), (21, 59), (22, 59), (23, 59), (21, 60), (22, 60), (23, 60), (21, 61), (22, 61), (23, 61)],
}