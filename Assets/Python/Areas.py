from Consts import *
from Core import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]
	
def getArea(iCiv, dRectangle, dExceptions, dPeriodRectangle=None, dPeriodExceptions=None):
	if dExceptions is None: dExceptions = appenddict()
	if dPeriodRectangle is None: dPeriodRectangle = appenddict()
	if dPeriodExceptions is None: dPeriodExceptions = appenddict()
	
	tBL, tTR = dRectangle[iCiv]
	lExceptions = dExceptions[iCiv]
	
	iPeriod = period(iCiv)
	if iPeriod in dPeriodRectangle:
		tBL, tTR = dPeriodRectangle[iPeriod]
		lExceptions = dPeriodExceptions[iPeriod]
	
	left, bottom = tBL
	right, top = tTR		
	return [(x, y) for x in range(left, right+1) for y in range(bottom, top+1) if (x, y) not in lExceptions]

def getCapital(iCiv):
	iPeriod = period(iCiv)
		
	if iPeriod in dPeriodCapitals:
		return dPeriodCapitals[iPeriod]
		
	return dCapitals[iCiv]
	
def getRespawnCapital(iCiv):
	if iCiv in dRespawnCapitals: return dRespawnCapitals[iCiv]
	return getCapital(iCiv)
	
def getNewCapital(iCiv):
	if iCiv in dNewCapitals: return dNewCapitals[iCiv]
	return getRespawnCapital(iCiv)
	
def getBirthArea(iCiv):
	return getArea(iCiv, dBirthArea, dBirthAreaExceptions)

def getBirthRectangle(iCiv, bExtended=None):
	if bExtended is None: bExtended = isExtendedBirth(slot(iCiv))
	if iCiv in dExtendedBirthArea and bExtended:
		return dExtendedBirthArea[iCiv]
	return dBirthArea[iCiv]
	
def getBirthExceptions(iCiv):
	if iCiv in dBirthAreaExceptions: return dBirthAreaExceptions[iCiv]
	return []
	
def getCoreArea(iCiv):
	return getArea(iCiv, dCoreArea, dCoreAreaExceptions, dPeriodCoreArea, dPeriodCoreAreaExceptions)
	
def getNormalArea(iCiv):
	return getArea(iCiv, dNormalArea, dNormalAreaExceptions, dPeriodNormalArea, dPeriodNormalAreaExceptions)

def getBroaderArea(iCiv):
	return getArea(iCiv, dBroaderArea, None, dPeriodBroaderArea)
	
def getRespawnArea(iCiv):
	if iCiv in dRespawnArea: return getArea(iCiv, dRespawnArea, appenddict())
	return getNormalArea(iCiv)
	
def updateCore(iPlayer):
	lCore = getCoreArea(civ(iPlayer))
	for plot in plots.all():
		if plot.isWater() or (plot.isPeak() and location(plot) not in lPeakExceptions): continue
		plot.setCore(iPlayer, location(plot) in lCore)
			
def isForeignCore(iPlayer, tPlot):
	return players.major().without(iPlayer).any(lambda p: plot(tPlot).isCore(p))
	
def isExtendedBirth(iPlayer):
	if human() == iPlayer: return False
	
	# add special conditions for extended AI flip zones here
	if civ(iPlayer) == iCivOttomans and player(iCivByzantium).isAlive(): return False
	
	return True
			
def init():
	for iPlayer in players.major():
		updateCore(iPlayer)
	
### Capitals ###

dCapitals = {
iCivEgypt :			(69, 33), # Thebes
iCivBabylonia :		(76, 40), # Babylon
iCivHarappa :		(87, 40), # Harappa
iCivChina :			(100, 44), # Chang'an
iCivGreece :		(67, 41), # Athens
iCivIndia :			(94, 40), # Pataliputra
iCivPhoenicia :		(73, 40), # Sur
iCivPolynesia :		(4, 18), # Tonga
iCivPersia :		(82, 38), # Persepolis
iCivRome :			(60, 44), # Rome
iCivMaya :			(22, 35), # Tikal
iCivTamils :		(91, 30), # Thanjavur
iCivEthiopia :		(72, 30), # Aksum
iCivKorea :			(109, 46), # Seoul
iCivByzantium :		(68, 45), # Constantinople
iCivJapan :			(113, 45), # Kyoto
iCivVikings :		(60, 59), # Oslo
iCivTurks :			(88, 49), # Orduqent
iCivArabia :		(75, 33), # Mecca
iCivTibet :			(96, 43), # Lhasa
iCivIndonesia :		(100, 26), # Palembang
iCivMoors :			(51, 41), # Cordoba
iCivSpain :			(52, 44), # Madrid
iCivFrance :		(55, 50), # Paris
iCivKhmer :			(102, 33), # Angkor
iCivEngland :		(53, 54), # London
iCivHolyRome :		(59, 51), # Frankfurt
iCivRussia :		(73, 54), # Moskow
iCivMali :			(51, 30), # Djenne
iCivPoland :		(65, 51), # Krakow
iCivPortugal :		(49, 43), # Lisboa
iCivInca :			(28, 22), # Cuzco
iCivItaly :			(59, 46), # Florence
iCivMongols :		(99, 51), # Karakorum
iCivAztecs :		(18, 37), # Tenochtitlan
iCivMughals : 		(90, 40), # Delhi
iCivOttomans : 		(70, 43), # Sogut
iCivThailand : 		(101, 33), # Ayutthaya
iCivCongo : 		(62, 20), # Mbanza Kongo
iCivIran : 			(81, 41), # Esfahan
iCivNetherlands :	(57, 53), # Amsterdam
iCivGermany : 		(62, 53), # Berlin
iCivAmerica :		(27, 46), # Washington
iCivArgentina :		(34, 11), # Buenos Aires
iCivMexico :		(18, 37), # Mexico City
iCivColombia :		(27, 29), # Bogota
iCivBrazil :		(41, 18), # Rio de Janeiro
iCivCanada :		(30, 52), # Montreal
}

dPeriodCapitals = {
iPeriodMing :			(102, 47), # Beijing
iPeriodMaratha :		(90, 40),	# Delhi
iPeriodCarthage : 		(58, 39),	# Carthage
iPeriodVijayanagara :	(90, 30),	# Vijayanagara
iPeriodVietnam :		(101, 37),	# Hanoi
iPeriodAustria :		(62, 49),	# Vienna
}

# new capital locations if changed during the game
dNewCapitals = {
iCivJapan :		(116, 46),	# Tokyo
iCivVikings :	(63, 59),	# Stockholm
iCivHolyRome :	(62, 49),	# Vienna
iCivItaly :		(60, 44),	# Rome
iCivMongols :	(102, 47),	# Khanbaliq
iCivOttomans :	(68, 45),	# Istanbul
}

# new capital locations on respawn
dRespawnCapitals = {
iCivEgypt :		(69, 35),	# Cairo
iCivChina :		(102, 47),	# Beijing
iCivIndia :		(90, 40),	# Delhi
iCivPersia :	(81, 41),	# Esfahan
iCivEthiopia :	(72, 28),	# Addis Ababa
iCivJapan :		(116, 46),	# Tokyo
iCivVikings :	(63, 59),	# Stockholm
iCivTurks : 	(84, 41),	# Herat
iCivIndonesia :	(104, 25),	# Jakarta
iCivMoors :		(51, 37),	# Marrakesh
iCivHolyRome :	(62, 49),	# Vienna
iCivInca :		(26, 22),	# Lima
iCivItaly :		(60, 44),	# Rome
iCivMughals :	(85, 37),	# Karachi
iCivOttomans :	(68, 45),	# Istanbul
}

### Birth Area ###

dBirthArea = {
iCivEgypt : 		((66, 30), 	(70, 36)),
iCivBabylonia : 	((75, 39), 	(77, 42)),
iCivHarappa : 		((85, 37), 	(88, 41)),
iCivChina : 		((99, 43), 	(107, 47)),
iCivGreece : 		((65, 39), 	(70, 45)),
iCivIndia : 		((87, 36), 	(96, 40)),
iCivCarthage : 		((71, 39), 	(74, 41)),
iCivPolynesia : 	((3, 17), 	(7, 22)),
iCivPersia : 		((79, 37), 	(85, 44)),
iCivRome : 			((59, 41), 	(63, 47)),
iCivMaya : 			((20, 35), 	(23, 37)),
iCivTamils : 		((90, 27), 	(93, 32)),
iCivEthiopia : 		((70, 27),	(73, 30)),
iCivKorea : 		((107, 45), (110, 49)),
iCivByzantium : 	((64, 38), 	(74, 45)),
iCivJapan : 		((111, 41), (116, 49)),
iCivVikings : 		((58, 56), 	(64, 62)),
iCivTurks : 		((79, 45),	(98, 52)),
iCivArabia : 		((67, 30), 	(80, 40)),
iCivTibet : 		((92, 41), 	(98, 45)),
iCivIndonesia : 	((98, 24), 	(107, 31)),
iCivMoors : 		((51, 37), 	(58, 43)),
iCivSpain : 		((49, 43), 	(53, 46)),
iCivFrance : 		((51, 46), 	(57, 52)),
iCivKhmer : 		((100, 32), (103, 36)),
iCivEngland : 		((50, 53), 	(54, 60)),
iCivHolyRome : 		((58, 48), 	(64, 54)),
iCivRussia : 		((67, 50), 	(74, 58)),
iCivMali : 			((50, 29), 	(55, 32)),
iCivPoland : 		((63, 50), 	(67, 55)),
iCivPortugal : 		((44, 42), 	(50, 44)),
iCivInca : 			((26, 20), 	(29, 24)),
iCivItaly : 		((58, 45), 	(63, 47)),
iCivMongols : 		((87, 46), 	(105, 54)),
iCivAztecs : 		((15, 36), 	(20, 41)),
iCivMughals : 		((86, 38), 	(91, 43)),
iCivOttomans : 		((69, 41), 	(76, 48)),
iCivThailand : 		((100, 32), (103, 36)),
iCivCongo: 			((61, 19), 	(65, 22)),
iCivIran :			((78, 38),	(86, 43)),
iCivNetherlands :	((56, 52), 	(58, 54)),
iCivGermany : 		((58, 49), 	(65, 55)),
iCivAmerica : 		((25, 43), 	(32, 50)),
iCivArgentina : 	((31, 3), 	(35, 13)),
iCivMexico :		((11, 34), 	(23, 48)),
iCivColombia :		((23, 25), 	(31, 32)),
iCivBrazil : 		((36, 15), 	(43, 27)),
iCivCanada : 		((20, 50), 	(35, 60)),
}

dExtendedBirthArea = {
iCivPersia :	((74, 37), 	(85, 44)), 	# includes Assyria and Anatolia
iCivSpain : 	((49, 43), 	(55, 46)), 	# includes Catalonia
iCivInca : 		((26, 19), 	(31, 24)),
iCivMongols : 	((81, 45), 	(105, 54)), # 6 more west, 1 more south
iCivOttomans : 	((67, 41), 	(76, 48)), 	# 2 more west
iCivArgentina : ((29, 3), 	(35, 13)), 	# includes Chile
}

dBirthAreaExceptions = appenddict({
iCivBabylonia :		[(78, 41), (78, 42)],
iCivHarappa :		[(85, 41), (88, 37), (88, 38)],
iCivChina :			[(106, 47)],
iCivGreece :		[(64, 45), (65, 45), (66, 45)],
iCivPersia :		[(85, 37), (85, 38), (85, 39), (72, 39), (72, 40), (72, 41), (73, 41), (74, 41), (75, 41), (76, 41), (77, 41), (78, 41), (73, 40), (74, 40), (75, 40), (76, 40), (77, 40), (78, 40), (73, 39), (74, 39), (75, 39), (76, 39), (77, 39), (78, 39), (73, 38), (74, 38), (75, 38), (76, 38), (77, 38), (72, 37), (73, 37), (74, 37), (75, 37), (76, 37), (77, 37), (78, 37)],
iCivTamils :		[(90, 33), (90, 34), (91, 34)],
iCivTurks :			[(95, 45), (96, 45), (97, 45)],
iCivArabia :		[(82, 34), (73, 40), (71, 36), (72, 37), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30), (72, 30), (72, 31), (72, 32), (71, 32)],
iCivTibet :			[(98, 42)],
iCivIndonesia :		[(100, 31), (100, 30), (101, 29), (101, 30)],
iCivMoors :			[(58, 43), (58, 42)],
iCivSpain :			[(49, 41), (49, 42), (49, 43), (49, 44), (50, 43), (50, 44), (50, 42)],
iCivFrance :		[(55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46), (56, 52), (57, 52)],
iCivHolyRome :		[(64, 51), (64, 52), (64, 53), (64, 54)],
iCivRussia :		[(68, 58), (69, 58), (70, 58), (65, 55), (66, 55), (66, 56)],
iCivPoland :		[(63, 50), (64, 50)],
iCivItaly :			[(63,47), (63,46)],
iCivMongols :		[(99, 47), (100, 47), (101, 47), (102, 47), (103, 47), (99, 46), (100, 46), (101, 46), (102, 46), (103, 46), (104, 46), (99, 45), (100, 45), (101, 45), (102, 45), (103, 45), (104, 45), (105, 45), (106, 45)],
iCivMughals :		[(92, 43), (93, 42), (93, 43), (94, 42), (94, 43)],
iCivOttomans :		[(74, 48), (75, 48), (76, 48), (75, 47), (75, 48), (76, 41)],
iCivNetherlands :	[(57, 51), (58, 51)],
iCivGermany :		[(62, 49), (62, 50), (63, 49), (63, 50), (64, 49), (64, 50), (64, 51), (65, 49), (65, 50), (65, 51), (66, 49), (66, 50), (66, 51), (58, 52), (58, 53), (62, 51), (63, 51), (64, 53), (61, 49), (61, 50), (64, 52), (58, 54), (65, 52), (65, 53)],
iCivAmerica :		[(25, 48), (25, 49), (25, 50), (26, 48), (26, 49), (27, 49), (27, 50), (28, 50), (29, 50), (30, 50)],
iCivArgentina :		[(35, 4), (35, 12), (35, 13), (36, 12), (36, 13)],
iCivMexico :		[(17, 48), (18, 48), (19, 48), (20, 48), (21, 48), (22, 48), (23, 48), (18, 47), (19, 47), (20, 47), (21, 47), (22, 47), (23, 47), (18, 46), (19, 46), (20, 46), (21, 46), (22, 46), (23, 46), (21, 45), (22, 45), (23, 45), (22, 44), (23, 44), (22, 43), (23, 43), (23, 42), (22, 35), (21, 34), (22, 34), (23, 34)],
iCivBrazil :		[(36, 15), (36, 16)],
iCivCanada :		[(20, 50), (21, 50), (22, 50), (23, 50), (24, 50), (25, 50), (29, 50), (30, 50), (31, 50), (32, 50), (20, 51), (21, 51), (22, 51), (23, 51), (24, 51), (32, 51), (35, 53), (35, 54), (34, 55), (34, 56), (33, 56), (33, 57)],
})

### Core Area ###

dCoreArea = {
iCivEgypt :			((67, 32),	(69, 36)),
iCivBabylonia :		((75, 39),	(77, 42)),
iCivHarappa :		((85, 37),	(88, 41)),
iCivChina :			((99, 43),	(107, 47)),
iCivGreece :		((64, 39),	(70, 45)),
iCivIndia :			((90, 38),	(96, 40)),
iCivPhoenicia :		((73, 39),	(74, 41)),
iCivPolynesia :		((4, 18),	(6, 21)),
iCivPersia :		((79, 37),	(85, 44)),
iCivRome :			((59, 41),	(63, 47)),
iCivMaya :			((21, 35),	(23, 37)),
iCivTamils :		((90, 27),	(93, 32)),
iCivEthiopia :		((70, 27),	(73, 30)),
iCivKorea :			((108, 45),	(110, 48)),
iCivByzantium :		((64, 40),	(72, 46)),
iCivJapan :			((112, 45),	(116, 47)),
iCivVikings :		((58, 56),	(64, 62)),
iCivTurks :			((81, 44),	(89, 51)),
iCivArabia :		((72, 33),	(78, 42)),
iCivTibet :			((92, 42),	(98, 45)),
iCivIndonesia :		((98, 24),	(107, 30)),
iCivMoors :			((51, 37),	(53, 42)),
iCivSpain :			((49, 43),	(53, 46)),
iCivFrance :		((51, 46),	(57, 51)),
iCivKhmer :			((100, 32),	(103, 36)),
iCivEngland :		((50, 53),	(54, 60)),
iCivHolyRome :		((58, 49),	(63, 52)),
iCivRussia :		((68, 49),	(75, 59)),
iCivMali :			((50, 29), 	(55, 32)),
iCivPoland :		((63, 50),	(67, 55)),
iCivPortugal :		((44, 42),	(50, 44)),
iCivInca :			((26, 20),	(28, 22)),
iCivItaly :			((58, 45),	(62, 47)),
iCivMongols :		((95, 47),	(105, 52)),
iCivAztecs :		((16, 35),	(19, 38)),
iCivMughals :		((86, 38),	(91, 43)),
iCivOttomans :		((69, 42),	(76, 46)),
iCivThailand :		((100, 32),	(103, 36)),
iCivCongo :			((61, 19),	(65, 22)),
iCivIran:			((79, 38), 	(82, 42)),
iCivNetherlands :	((56, 52),	(58, 54)),
iCivGermany :		((58, 49),	(65, 55)),
iCivAmerica :		((23, 45),	(32, 50)),
iCivArgentina :		((31, 6),	(35, 12)),
iCivMexico :		((16, 35),	(19, 40)),
iCivColombia :		((24, 26),	(31, 32)),
iCivBrazil :		((37, 15),	(41, 22)),
iCivCanada :		((27, 50),	(35, 52)),
}

dPeriodCoreArea = {
iPeriodMing : 						((99, 42),	(107, 47)),
iPeriodModernGreece :				((65, 39), 	(69, 42)),
iPeriodMaratha : 					((88, 33),	(91, 38)),
iPeriodCarthage:					((54, 37),	(60, 39)),
iPeriodByzantineConstantinople :	((67, 44),	(69, 46)),
iPeriodMeiji : 						((111, 41),	(116, 49)),
iPeriodSeljuks : 					((79, 37),	(85, 44)),
iPeriodSaudi :						((73, 30),	(82, 36)),
iPeriodMorocco : 					((51, 37),	(56, 39)),
iPeriodSpain : 						((49, 40),	(55, 46)),
iPeriodVietnam : 					((97, 35),	(102, 38)),
iPeriodAustria : 					((61, 46),	(66, 51)),
iPeriodModernItaly : 				((58, 40),	(63, 47)),
iPeriodYuan : 						((95, 46),	(106, 52)),
iPeriodPakistan : 					((86, 37),	(94, 43)),
iPeriodOttomanConstantinople : 		((67, 42),	(76, 47)),
iPeriodModernGermany : 				((58, 49),	(63, 55)),
}

dCoreAreaExceptions = appenddict({
iCivHarappa :	[(85, 41), (88, 37), (88, 38)],
iCivChina :		[(99, 46), (99, 47), (104, 43), (105, 43), (106, 43), (107, 43), (105, 44), (106, 44), (106, 47)],
iCivGreece :	[(64, 45), (65, 45)],
iCivPersia :	[(85, 37), (85, 38), (85, 39)],
iCivByzantium :	[(71, 40)],
iCivTurks :		[(84, 36), (84, 37), (85, 36), (85, 37), (85, 38), (85, 39), (88, 44)],
iCivArabia :	[(72, 42), (73, 42), (74, 42), (77, 33), (78, 33), (77, 34), (78, 34), (76, 35), (77, 35), (78, 35), (76, 36), (77, 36), (78, 36), (76, 37), (77, 37), (78, 37)],
iCivTibet :		[(98, 42)],
iCivIndonesia :	[(100, 30), (101, 29), (101, 30)],
iCivSpain :		[(49, 43), (49, 44), (50, 43), (50, 44)],
iCivFrance :	[(51, 46), (52, 46), (55, 46), (57, 46)],
iCivHolyRome :	[(61, 52), (62, 52), (63, 52)],
iCivRussia :	[(68, 49), (68, 59), (69, 49), (69, 59), (70, 59), (71, 49)],
iCivPoland :	[(63, 50), (64, 50)],
iCivMongols :	[(102, 47), (103, 47)],
iCivMughals :	[(86, 43)],
iCivGermany :	[(58, 52), (58, 53), (58, 54), (61, 49), (61, 50), (62, 49), (62, 50), (62, 51), (63, 49), (63, 50), (63, 51), (64, 49), (64, 50), (64, 51), (64, 52), (64, 53), (65, 49), (65, 51), (65, 52), (65, 53)],
iCivAmerica :	[(23, 50), (27, 50), (29, 50), (30, 50)],
iCivArgentina :	[(35, 12)],
iCivMexico :	[(19, 40)],
iCivColombia :	[(30, 26), (30, 27), (30, 28), (30, 29), (31, 26), (31, 27)],
iCivCanada :	[(29, 50), (30, 50), (31, 50), (32, 50), (32, 51)],
})

dPeriodCoreAreaExceptions = appenddict({
iPeriodMing :					[(99, 46), (99, 47), (106, 47)],
iPeriodModernGreece :			[(64, 45), (65, 45), (66, 46)],
iPeriodSpain :					[(49, 41), (49, 42), (49, 43), (49, 44), (50, 42), (50, 43), (50, 44), (55, 46)],
iPeriodVietnam :				[(104, 39)],
iPeriodAustria :				[(61, 51), (64, 51), (65, 51), (66, 51)],
iPeriodModernItaly :			[(63, 46), (63, 47)],
iPeriodPakistan : 				[(92, 43), (93, 43), (94, 42), (94, 43)],
iPeriodOttomanConstantinople :	[(67, 42), (70, 42), (71, 42), (73, 42), (74, 42), (75, 42)],
iPeriodModernGermany :			[(58, 52), (58, 53), (58, 54), (61, 49), (61, 50), (62, 49), (62, 50), (62, 51), (63, 49), (63, 50), (63, 51)],
})

### Normal Area ###

dNormalArea = {
iCivEgypt :			((65, 30), 	(72, 37)),
iCivBabylonia :		((74, 38), 	(79, 44)),
iCivHarappa :		((84, 35), 	(88, 42)),
iCivChina :			((99, 39), 	(108, 50)),
iCivGreece :		((64, 39), 	(68, 44)),
iCivIndia :			((89, 38), 	(96, 42)),
iCivPhoenicia :		((72, 39), 	(74, 41)),
iCivPolynesia :		((3, 15), 	(13, 21)),
iCivPersia :		((79, 37), 	(86, 46)),
iCivRome :			((57, 40), 	(63, 47)),
iCivMaya :			((20, 32), 	(23, 37)),
iCivTamils :		((90, 28), 	(93, 34)),
iCivEthiopia :		((68, 25), 	(77, 30)),
iCivKorea :			((108, 45), (110, 49)),
iCivByzantium :		((64, 40), 	(72, 45)),
iCivJapan :			((111, 41), (116, 52)),
iCivVikings :		((58, 56), 	(67, 65)),
iCivTurks :			((79, 44),	(103, 52)),
iCivArabia :		((72, 30), 	(82, 38)),
iCivTibet :			((92, 41), 	(98, 45)),
iCivIndonesia :		((98, 24), 	(113, 31)),
iCivMoors :			((51, 37), 	(58, 43)),
iCivSpain :			((49, 40), 	(55, 46)),
iCivFrance :		((51, 46), 	(58, 52)),
iCivKhmer :			((98, 26), 	(103, 37)),
iCivEngland :		((50, 53), 	(54, 60)),
iCivHolyRome :		((58, 48), 	(65, 54)),
iCivRussia :		((68, 49), 	(83, 62)),
iCivMali :			((48, 28), 	(57, 34)),
iCivPoland :		((63, 50), 	(69, 55)),
iCivPortugal :		((44, 41), 	(50, 44)),
iCivInca :			((24, 14), 	(30, 29)),
iCivItaly :			((57, 40), 	(63, 47)),
iCivMongols :		((92, 48), 	(104, 54)),
iCivAztecs :		((15, 35), 	(20, 40)),
iCivMughals :		((86, 37), 	(94, 43)),
iCivOttomans :		((68, 42), 	(78, 49)),
iCivThailand :		((99, 31), 	(103, 37)),
iCivCongo :			((61, 19), 	(65, 22)),
iCivIran :			((79, 37), 	(86, 46)),
iCivNetherlands :	((56, 51), 	(58, 54)),
iCivGermany :		((59, 48), 	(66, 55)),
iCivAmerica :		((11, 43), 	(31, 49)),
iCivArgentina :		((31,  3), 	(36, 15)),
iCivMexico :		((15, 35), 	(20, 40)),
iCivColombia :		((24, 26),	(29, 32)),
iCivBrazil :		((32, 14), 	(43, 28)),
iCivCanada :		(( 8, 50), 	(37, 67)),
}

dPeriodNormalArea = {
iPeriodMaratha : 	((96, 42),	(97, 42)),
iPeriodCarthage :	((71, 39),	(74, 41)),
iPeriodSaudi : 		((73, 30),	(82, 38)),
iPeriodAustria :	((61, 46),	(66, 50)),
}

dNormalAreaExceptions = appenddict({
iCivEgypt :		[(72, 37), (70, 30), (71, 30), (72, 30)],
iCivHarappa :	[(84, 41), (84, 42), (84, 43), (85, 41), (85, 42), (85, 43), (86, 43)],
iCivChina :		[(99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50), (100, 39), (101, 39)],
iCivIndia :		[(93, 42), (94, 42), (95, 42), (96, 42)],
iCivPolynesia :	[(13, 21)],
iCivPersia :	[(86, 39), (86, 38), (86, 37)],
iCivRome :		[(62, 47), (63, 47), (63, 46)],
iCivEthiopia :	[(76, 30), (77, 30)],
iCivJapan :		[(111, 52), (112, 52), (111, 51)],
iCivVikings :	[(65, 56), (66, 56), (67, 56), (66, 57), (67, 57)],
iCivTurks :		[(88, 44), (93, 44), (94, 44), (95, 44), (96, 44), (97, 44), (98, 44), (95, 45), (96, 45), (97, 45), (100, 44), (101, 44), (102, 44), (103, 44), (100, 45), (101, 45), (102, 45), (103, 45), (99, 46), (101, 46), (102, 46), (103, 46), (99, 47), (100, 47), (101, 47), (102, 47), (103, 47), (99, 48), (100, 48), (101, 48), (102, 48), (103, 48), (100, 49), (101, 49), (102, 49), (103, 49)],
iCivArabia :	[(81, 38), (82, 38), (82, 37)],
iCivSpain :		[(49, 44), (49, 43), (49, 42), (49, 41)],
iCivFrance :	[(51, 46), (52, 46), (53, 46), (58, 47), (58, 46), (58, 51), (58, 52), (57, 52)],
iCivRussia :	[(80, 49), (68, 62), (68, 61), (68, 60), (68, 59)],
iCivPoland :	[(63, 50), (64, 50)],
iCivItaly :		[(62, 47), (63, 47), (63, 46)],
iCivMongols :	[(92, 52), (92, 53), (92, 54), (93, 54), (94, 54), (100, 48), (101, 48), (102, 48), (103, 48), (104, 48)],
iCivAztecs :	[(20, 35)],
iCivMexico :	[(20, 35)],
iCivArgentina :	[(35, 12), (35, 13), (36, 12), (36, 13), (36, 14), (36, 15)],
iCivCanada :	[(11,50), (12,50), (13,50), (14,50), (16,50), (17,50), (18,50), (19,50), (20,50), (21,50), (22,50), (23,50), (24,50), (25,50), (29,50), (30,50), (31,50), (32,50), (32,51), (8,59), (8,60), (8,61), (8,62), (8,63), (8,64), (8,65), (9,59), (9,60), (9,61), (9,62), (9,63), (9,64), (9,65), (37,66), (37,67)],
})

dPeriodNormalAreaExceptions = appenddict({
iPeriodMing : [(99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50)],
})

### Broader Area ###

dBroaderArea = {
iCivEgypt :			((60, 26), 	(74, 38)),
iCivBabylonia :		((72, 37), 	(78, 44)),
iCivHarappa :		((90, 40), 	(90, 40)),
iCivChina :			((95, 38), 	(108, 50)),
iCivGreece :		((62, 39), 	(77, 47)),
iCivIndia :			((85, 28), 	(99, 43)),
iCivPhoenicia :		((71, 39), 	(74, 41)),
iCivPolynesia :		((1, 15), 	(17, 38)),
iCivPersia :		((70, 37), 	(87, 49)),
iCivRome :			((49, 35), 	(73, 50)),
iCivMaya :			((19, 30), 	(26, 37)),
iCivTamils :		((90, 28), 	(93, 34)),
iCivEthiopia :		((67, 21), 	(77, 30)),
iCivKorea :			((106, 45), (110, 52)),
iCivByzantium :		((58, 34), 	(74, 45)),
iCivJapan :			((110, 40), (116, 56)),
iCivVikings :		((58, 56), 	(71, 65)),
iCivTurks :			((79, 44),	(103, 52)),
iCivArabia :		((64, 30), 	(85, 44)),
iCivTibet :			((92, 41), 	(98, 45)),
iCivIndonesia :		((98, 24), 	(113, 31)),
iCivMoors :			((51, 37), 	(58, 43)),
iCivSpain :			((49, 38), 	(55, 46)),
iCivFrance :		((49, 44), 	(61, 52)),
iCivKhmer :			((97, 25), 	(105, 39)),
iCivEngland :		((48, 53), 	(54, 60)),
iCivHolyRome :		((58, 43), 	(64, 54)),
iCivRussia :		((65, 48), 	(92, 59)),
iCivMali :			((48, 26), 	(59, 34)),
iCivPoland :		((63, 50), 	(67, 55)),
iCivPortugal :		((49, 40), 	(51, 45)),
iCivInca :			((24, 14), 	(30, 27)),
iCivItaly :			((57, 47), 	(65, 47)),
iCivMongols :		((82, 44), 	(110, 62)),
iCivAztecs :		((14, 32), 	(24, 43)),
iCivMughals :		((86, 37), 	(94, 43)),
iCivOttomans :		((68, 42), 	(86, 49)),
iCivThailand :		((97, 25), 	(105, 39)),
iCivCongo :			((61, 19), 	(65, 22)),
iCivNetherlands :	((56, 51), 	(58, 54)),
iCivGermany :		((55, 46), 	(67, 57)),
iCivAmerica :		((10, 42), 	(37, 56)),
iCivArgentina :		((29,  3), 	(36, 15)),
iCivColombia :		((33, 32),	(33, 32)),
iCivBrazil :		((32, 14), 	(43, 28)),
iCivCanada :		(( 8, 50), 	(37, 67)),
}

dPeriodBroaderArea = {
iPeriodByzantineConstantinople : 	((64, 38),	(74, 45)),
iPeriodAustria :	((61, 46),	(66, 50)),
iPeriodPakistan :	((84, 37),	(94, 43)),
}

### Respawn area ###

dRespawnArea = {
iCivEgypt :		((65, 30),	(71, 38)),
iCivChina :		((99, 39),	(107, 47)),
iCivIndia :		((88, 33),	(96, 41)),
iCivByzantium :	((65, 40),	(69, 46)),
iCivTurks :		((81, 41),	(86, 48)),
iCivMoors :		((48, 34),	(58, 39)),
iCivInca :		((25, 16),	(33, 25)),
iCivMughals :	((85, 37),	(88, 43)),
}

### Rebirth area ###

dRebirthArea = {
}

dRebirthAreaExceptions = appenddict({
})