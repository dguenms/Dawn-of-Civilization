from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]
	
### Capitals ###

dCapitals = CivDict({
iEgypt :		(69, 33), # Thebes
iBabylonia :	(76, 40), # Babylon
iHarappa :		(87, 40), # Harappa
iChina :		(100, 44), # Chang'an
iGreece :		(67, 41), # Athens
iIndia :		(94, 40), # Pataliputra
iPhoenicia :	(73, 40), # Sur
iPolynesia :	(4, 18), # Tonga
iPersia :		(82, 38), # Persepolis
iRome :			(60, 44), # Rome
iMaya :			(22, 35), # Tikal
iTamils :		(91, 30), # Thanjavur
iEthiopia :		(72, 30), # Aksum
iKorea :		(109, 46), # Seoul
iByzantium :	(68, 45), # Constantinople
iJapan :		(113, 45), # Kyoto
iVikings :		(60, 59), # Oslo
iTurks :		(88, 49), # Orduqent
iArabia :		(75, 33), # Mecca
iTibet :		(96, 43), # Lhasa
iIndonesia :	(100, 26), # Palembang
iMoors :		(51, 41), # Cordoba
iSpain :		(52, 44), # Madrid
iFrance :		(55, 50), # Paris
iKhmer :		(102, 33), # Angkor
iEngland :		(53, 54), # London
iHolyRome :		(59, 51), # Frankfurt
iRussia :		(73, 54), # Moskow
iMali :			(51, 30), # Djenne
iPoland :		(65, 51), # Krakow
iPortugal :		(49, 43), # Lisboa
iInca :			(28, 22), # Cuzco
iItaly :		(59, 46), # Florence
iMongols :		(99, 51), # Karakorum
iAztecs :		(18, 37), # Tenochtitlan
iMughals : 		(90, 40), # Delhi
iOttomans : 	(70, 43), # Sogut
iThailand : 	(101, 33), # Ayutthaya
iCongo : 		(62, 20), # Mbanza Kongo
iIran : 		(81, 41), # Esfahan
iNetherlands :	(57, 53), # Amsterdam
iGermany : 		(62, 53), # Berlin
iAmerica :		(27, 46), # Washington
iArgentina :	(34, 11), # Buenos Aires
iMexico :		(18, 37), # Mexico City
iColombia :		(27, 29), # Bogota
iBrazil :		(41, 18), # Rio de Janeiro
iCanada :		(30, 52), # Montreal
})

dPeriodCapitals = {
iPeriodMing :			(102, 47), # Beijing
iPeriodMaratha :		(90, 40),	# Delhi
iPeriodCarthage : 		(58, 39),	# Carthage
iPeriodVijayanagara :	(90, 30),	# Vijayanagara
iPeriodVietnam :		(101, 37),	# Hanoi
iPeriodAustria :		(62, 49),	# Vienna
}

# new capital locations if changed during the game
dNewCapitals = CivDict({
iJapan :	(116, 46),	# Tokyo
iVikings :	(63, 59),	# Stockholm
iHolyRome :	(62, 49),	# Vienna
iItaly :	(60, 44),	# Rome
iMongols :	(102, 47),	# Khanbaliq
iOttomans :	(68, 45),	# Istanbul
})

# new capital locations on respawn
dRespawnCapitals = CivDict({
iEgypt :	(69, 35),	# Cairo
iChina :	(102, 47),	# Beijing
iIndia :	(90, 40),	# Delhi
iPersia :	(81, 41),	# Esfahan
iEthiopia :	(72, 28),	# Addis Ababa
iJapan :	(116, 46),	# Tokyo
iVikings :	(63, 59),	# Stockholm
iTurks : 	(84, 41),	# Herat
iIndonesia :(104, 25),	# Jakarta
iMoors :	(51, 37),	# Marrakesh
iHolyRome :	(62, 49),	# Vienna
iInca :		(26, 22),	# Lima
iItaly :	(60, 44),	# Rome
iMughals :	(85, 37),	# Karachi
iOttomans :	(68, 45),	# Istanbul
})

### Birth Area ###

dBirthArea = CivDict({
iEgypt : 		((66, 30), 	(70, 36)),
iBabylonia : 	((75, 39), 	(77, 42)),
iHarappa : 		((85, 37), 	(88, 41)),
iChina : 		((99, 43), 	(107, 47)),
iGreece : 		((65, 39), 	(70, 45)),
iIndia : 		((87, 36), 	(96, 40)),
iCarthage : 	((71, 39), 	(74, 41)),
iPolynesia : 	((3, 17), 	(7, 22)),
iPersia : 		((79, 37), 	(85, 44)),
iRome : 		((59, 41), 	(63, 47)),
iMaya : 		((20, 35), 	(23, 37)),
iTamils : 		((90, 27), 	(93, 32)),
iEthiopia : 	((70, 27),	(73, 30)),
iKorea : 		((107, 45), (110, 49)),
iByzantium : 	((64, 38), 	(74, 45)),
iJapan : 		((111, 41), (116, 49)),
iVikings : 		((58, 56), 	(64, 62)),
iTurks : 		((79, 45),	(98, 52)),
iArabia : 		((67, 30), 	(80, 40)),
iTibet : 		((92, 41), 	(98, 45)),
iIndonesia : 	((98, 24), 	(107, 31)),
iMoors : 		((51, 37), 	(58, 43)),
iSpain : 		((49, 43), 	(53, 46)),
iFrance : 		((51, 46), 	(57, 52)),
iKhmer : 		((100, 32), (103, 36)),
iEngland : 		((50, 53), 	(54, 60)),
iHolyRome : 	((58, 48), 	(64, 54)),
iRussia : 		((67, 50), 	(74, 58)),
iMali : 		((50, 29), 	(55, 32)),
iPoland : 		((63, 50), 	(67, 55)),
iPortugal : 	((44, 42), 	(50, 44)),
iInca : 		((26, 20), 	(29, 24)),
iItaly : 		((58, 45), 	(63, 47)),
iMongols : 		((87, 46), 	(105, 54)),
iAztecs : 		((15, 36), 	(20, 41)),
iMughals : 		((86, 38), 	(91, 43)),
iOttomans : 	((69, 41), 	(76, 48)),
iThailand : 	((100, 32), (103, 36)),
iCongo: 		((61, 19), 	(65, 22)),
iIran :			((78, 38),	(86, 43)),
iNetherlands :	((56, 52), 	(58, 54)),
iGermany : 		((58, 49), 	(65, 55)),
iAmerica : 		((25, 43), 	(32, 50)),
iArgentina : 	((31, 3), 	(35, 13)),
iMexico :		((11, 34), 	(23, 48)),
iColombia :		((23, 25), 	(31, 32)),
iBrazil : 		((36, 15), 	(43, 27)),
iCanada : 		((20, 50), 	(35, 60)),
})

dExtendedBirthArea = CivDict({
iPersia :	((74, 37), 	(85, 44)), 	# includes Assyria and Anatolia
iSpain : 	((49, 43), 	(55, 46)), 	# includes Catalonia
iInca : 	((26, 19), 	(31, 24)),
iMongols : 	((81, 45), 	(105, 54)), # 6 more west, 1 more south
iOttomans : ((67, 41), 	(76, 48)), 	# 2 more west
iArgentina :((29, 3), 	(35, 13)), 	# includes Chile
})

dBirthAreaExceptions = CivDict({
iBabylonia :	[(78, 41), (78, 42)],
iHarappa :		[(85, 41), (88, 37), (88, 38)],
iChina :		[(106, 47)],
iGreece :		[(64, 45), (65, 45), (66, 45)],
iPersia :		[(85, 37), (85, 38), (85, 39), (72, 39), (72, 40), (72, 41), (73, 41), (74, 41), (75, 41), (76, 41), (77, 41), (78, 41), (73, 40), (74, 40), (75, 40), (76, 40), (77, 40), (78, 40), (73, 39), (74, 39), (75, 39), (76, 39), (77, 39), (78, 39), (73, 38), (74, 38), (75, 38), (76, 38), (77, 38), (72, 37), (73, 37), (74, 37), (75, 37), (76, 37), (77, 37), (78, 37)],
iTamils :		[(90, 33), (90, 34), (91, 34)],
iTurks :		[(95, 45), (96, 45), (97, 45)],
iArabia :		[(82, 34), (73, 40), (71, 36), (72, 37), (67, 30), (68, 30), (69, 30), (70, 30), (71, 30), (72, 30), (72, 31), (72, 32), (71, 32)],
iTibet :		[(98, 42)],
iIndonesia :	[(100, 31), (100, 30), (101, 29), (101, 30)],
iMoors :		[(58, 43), (58, 42)],
iSpain :		[(49, 41), (49, 42), (49, 43), (49, 44), (50, 43), (50, 44), (50, 42)],
iFrance :		[(55, 46), (57, 46), (56, 45), (57, 45), (58, 48), (58, 49), (58, 50), (53, 46), (52, 46), (51, 46), (57, 46), (56, 52), (57, 52)],
iHolyRome :		[(64, 51), (64, 52), (64, 53), (64, 54)],
iRussia :		[(68, 58), (69, 58), (70, 58), (65, 55), (66, 55), (66, 56)],
iPoland :		[(63, 50), (64, 50)],
iItaly :		[(63,47), (63,46)],
iMongols :		[(99, 47), (100, 47), (101, 47), (102, 47), (103, 47), (99, 46), (100, 46), (101, 46), (102, 46), (103, 46), (104, 46), (99, 45), (100, 45), (101, 45), (102, 45), (103, 45), (104, 45), (105, 45), (106, 45)],
iMughals :		[(92, 43), (93, 42), (93, 43), (94, 42), (94, 43)],
iOttomans :		[(74, 48), (75, 48), (76, 48), (75, 47), (75, 48), (76, 41)],
iNetherlands :	[(57, 51), (58, 51)],
iGermany :		[(62, 49), (62, 50), (63, 49), (63, 50), (64, 49), (64, 50), (64, 51), (65, 49), (65, 50), (65, 51), (66, 49), (66, 50), (66, 51), (58, 52), (58, 53), (62, 51), (63, 51), (64, 53), (61, 49), (61, 50), (64, 52), (58, 54), (65, 52), (65, 53)],
iAmerica :		[(25, 48), (25, 49), (25, 50), (26, 48), (26, 49), (27, 49), (27, 50), (28, 50), (29, 50), (30, 50)],
iArgentina :	[(35, 4), (35, 12), (35, 13), (36, 12), (36, 13)],
iMexico :		[(17, 48), (18, 48), (19, 48), (20, 48), (21, 48), (22, 48), (23, 48), (18, 47), (19, 47), (20, 47), (21, 47), (22, 47), (23, 47), (18, 46), (19, 46), (20, 46), (21, 46), (22, 46), (23, 46), (21, 45), (22, 45), (23, 45), (22, 44), (23, 44), (22, 43), (23, 43), (23, 42), (22, 35), (21, 34), (22, 34), (23, 34)],
iBrazil :		[(36, 15), (36, 16)],
iCanada :		[(20, 50), (21, 50), (22, 50), (23, 50), (24, 50), (25, 50), (29, 50), (30, 50), (31, 50), (32, 50), (20, 51), (21, 51), (22, 51), (23, 51), (24, 51), (32, 51), (35, 53), (35, 54), (34, 55), (34, 56), (33, 56), (33, 57)],
}, [])

### Core Area ###

dCoreArea = CivDict({
iEgypt :		((67, 32),	(69, 36)),
iBabylonia :	((75, 39),	(77, 42)),
iHarappa :		((85, 37),	(88, 41)),
iChina :		((99, 43),	(107, 47)),
iGreece :		((64, 39),	(70, 45)),
iIndia :		((90, 38),	(96, 40)),
iPhoenicia :	((73, 39),	(74, 41)),
iPolynesia :	((4, 18),	(6, 21)),
iPersia :		((79, 37),	(85, 44)),
iRome :			((59, 41),	(63, 47)),
iMaya :			((21, 35),	(23, 37)),
iTamils :		((90, 27),	(93, 32)),
iEthiopia :		((70, 27),	(73, 30)),
iKorea :		((108, 45),	(110, 48)),
iByzantium :	((64, 40),	(72, 46)),
iJapan :		((112, 45),	(116, 47)),
iVikings :		((58, 56),	(64, 62)),
iTurks :		((81, 44),	(89, 51)),
iArabia :		((72, 33),	(78, 42)),
iTibet :		((92, 42),	(98, 45)),
iIndonesia :	((98, 24),	(107, 30)),
iMoors :		((51, 37),	(53, 42)),
iSpain :		((49, 43),	(53, 46)),
iFrance :		((51, 46),	(57, 51)),
iKhmer :		((100, 32),	(103, 36)),
iEngland :		((50, 53),	(54, 60)),
iHolyRome :		((58, 49),	(63, 52)),
iRussia :		((68, 49),	(75, 59)),
iMali :			((50, 29), 	(55, 32)),
iPoland :		((63, 50),	(67, 55)),
iPortugal :		((44, 42),	(50, 44)),
iInca :			((26, 20),	(28, 22)),
iItaly :		((58, 45),	(62, 47)),
iMongols :		((95, 47),	(105, 52)),
iAztecs :		((16, 35),	(19, 38)),
iMughals :		((86, 38),	(91, 43)),
iOttomans :		((69, 42),	(76, 46)),
iThailand :		((100, 32),	(103, 36)),
iCongo :		((61, 19),	(65, 22)),
iIran:			((79, 38), 	(82, 42)),
iNetherlands :	((56, 52),	(58, 54)),
iGermany :		((58, 49),	(65, 55)),
iAmerica :		((23, 45),	(32, 50)),
iArgentina :	((31, 6),	(35, 12)),
iMexico :		((16, 35),	(19, 40)),
iColombia :		((24, 26),	(31, 32)),
iBrazil :		((37, 15),	(41, 22)),
iCanada :		((27, 50),	(35, 52)),
})

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

dCoreAreaExceptions = CivDict({
iHarappa :	[(85, 41), (88, 37), (88, 38)],
iChina :	[(99, 46), (99, 47), (104, 43), (105, 43), (106, 43), (107, 43), (105, 44), (106, 44), (106, 47)],
iGreece :	[(64, 45), (65, 45)],
iPersia :	[(85, 37), (85, 38), (85, 39)],
iByzantium :[(71, 40)],
iTurks :	[(84, 36), (84, 37), (85, 36), (85, 37), (85, 38), (85, 39), (88, 44)],
iArabia :	[(72, 42), (73, 42), (74, 42), (77, 33), (78, 33), (77, 34), (78, 34), (76, 35), (77, 35), (78, 35), (76, 36), (77, 36), (78, 36), (76, 37), (77, 37), (78, 37)],
iTibet :	[(98, 42)],
iIndonesia :[(100, 30), (101, 29), (101, 30)],
iSpain :	[(49, 43), (49, 44), (50, 43), (50, 44)],
iFrance :	[(51, 46), (52, 46), (55, 46), (57, 46)],
iHolyRome :	[(61, 52), (62, 52), (63, 52)],
iRussia :	[(68, 49), (68, 59), (69, 49), (69, 59), (70, 59), (71, 49)],
iPoland :	[(63, 50), (64, 50)],
iMongols :	[(102, 47), (103, 47)],
iMughals :	[(86, 43)],
iGermany :	[(58, 52), (58, 53), (58, 54), (61, 49), (61, 50), (62, 49), (62, 50), (62, 51), (63, 49), (63, 50), (63, 51), (64, 49), (64, 50), (64, 51), (64, 52), (64, 53), (65, 49), (65, 51), (65, 52), (65, 53)],
iAmerica :	[(23, 50), (27, 50), (29, 50), (30, 50)],
iArgentina :[(35, 12)],
iMexico :	[(19, 40)],
iColombia :	[(30, 26), (30, 27), (30, 28), (30, 29), (31, 26), (31, 27)],
iCanada :	[(29, 50), (30, 50), (31, 50), (32, 50), (32, 51)],
}, [])

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

dNormalArea = CivDict({
iEgypt :		((65, 30), 	(72, 37)),
iBabylonia :	((74, 38), 	(79, 44)),
iHarappa :		((84, 35), 	(88, 42)),
iChina :		((99, 39), 	(108, 50)),
iGreece :		((64, 39), 	(68, 44)),
iIndia :		((89, 38), 	(96, 42)),
iPhoenicia :	((72, 39), 	(74, 41)),
iPolynesia :	((3, 15), 	(13, 21)),
iPersia :		((79, 37), 	(86, 46)),
iRome :			((57, 40), 	(63, 47)),
iMaya :			((20, 32), 	(23, 37)),
iTamils :		((90, 28), 	(93, 34)),
iEthiopia :		((68, 25), 	(77, 30)),
iKorea :		((108, 45), (110, 49)),
iByzantium :	((64, 40), 	(72, 45)),
iJapan :		((111, 41), (116, 52)),
iVikings :		((58, 56), 	(67, 65)),
iTurks :		((79, 44),	(103, 52)),
iArabia :		((72, 30), 	(82, 38)),
iTibet :		((92, 41), 	(98, 45)),
iIndonesia :	((98, 24), 	(113, 31)),
iMoors :		((51, 37), 	(58, 43)),
iSpain :		((49, 40), 	(55, 46)),
iFrance :		((51, 46), 	(58, 52)),
iKhmer :		((98, 26), 	(103, 37)),
iEngland :		((50, 53), 	(54, 60)),
iHolyRome :		((58, 48), 	(65, 54)),
iRussia :		((68, 49), 	(83, 62)),
iMali :			((48, 28), 	(57, 34)),
iPoland :		((63, 50), 	(69, 55)),
iPortugal :		((44, 41), 	(50, 44)),
iInca :			((24, 14), 	(30, 29)),
iItaly :		((57, 40), 	(63, 47)),
iMongols :		((92, 48), 	(104, 54)),
iAztecs :		((15, 35), 	(20, 40)),
iMughals :		((86, 37), 	(94, 43)),
iOttomans :		((68, 42), 	(78, 49)),
iThailand :		((99, 31), 	(103, 37)),
iCongo :		((61, 19), 	(65, 22)),
iIran :			((79, 37), 	(86, 46)),
iNetherlands :	((56, 51), 	(58, 54)),
iGermany :		((59, 48), 	(66, 55)),
iAmerica :		((11, 43), 	(31, 49)),
iArgentina :	((31,  3), 	(36, 15)),
iMexico :		((15, 35), 	(20, 40)),
iColombia :		((24, 26),	(29, 32)),
iBrazil :		((32, 14), 	(43, 28)),
iCanada :		(( 8, 50), 	(37, 67)),
})

dPeriodNormalArea = {
iPeriodMaratha : 	((96, 42),	(97, 42)),
iPeriodCarthage :	((71, 39),	(74, 41)),
iPeriodSaudi : 		((73, 30),	(82, 38)),
iPeriodAustria :	((61, 46),	(66, 50)),
}

dNormalAreaExceptions = CivDict({
iEgypt :	[(72, 37), (70, 30), (71, 30), (72, 30)],
iHarappa :	[(84, 41), (84, 42), (84, 43), (85, 41), (85, 42), (85, 43), (86, 43)],
iChina :	[(99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50), (100, 39), (101, 39)],
iIndia :	[(93, 42), (94, 42), (95, 42), (96, 42)],
iPolynesia :[(13, 21)],
iPersia :	[(86, 39), (86, 38), (86, 37)],
iRome :		[(62, 47), (63, 47), (63, 46)],
iEthiopia :	[(76, 30), (77, 30)],
iJapan :	[(111, 52), (112, 52), (111, 51)],
iVikings :	[(65, 56), (66, 56), (67, 56), (66, 57), (67, 57)],
iTurks :	[(88, 44), (93, 44), (94, 44), (95, 44), (96, 44), (97, 44), (98, 44), (95, 45), (96, 45), (97, 45), (100, 44), (101, 44), (102, 44), (103, 44), (100, 45), (101, 45), (102, 45), (103, 45), (99, 46), (101, 46), (102, 46), (103, 46), (99, 47), (100, 47), (101, 47), (102, 47), (103, 47), (99, 48), (100, 48), (101, 48), (102, 48), (103, 48), (100, 49), (101, 49), (102, 49), (103, 49)],
iArabia :	[(81, 38), (82, 38), (82, 37)],
iSpain :	[(49, 44), (49, 43), (49, 42), (49, 41)],
iFrance :	[(51, 46), (52, 46), (53, 46), (58, 47), (58, 46), (58, 51), (58, 52), (57, 52)],
iRussia :	[(80, 49), (68, 62), (68, 61), (68, 60), (68, 59)],
iPoland :	[(63, 50), (64, 50)],
iItaly :	[(62, 47), (63, 47), (63, 46)],
iMongols :	[(92, 52), (92, 53), (92, 54), (93, 54), (94, 54), (100, 48), (101, 48), (102, 48), (103, 48), (104, 48)],
iAztecs :	[(20, 35)],
iMexico :	[(20, 35)],
iArgentina :[(35, 12), (35, 13), (36, 12), (36, 13), (36, 14), (36, 15)],
iCanada :	[(11,50), (12,50), (13,50), (14,50), (16,50), (17,50), (18,50), (19,50), (20,50), (21,50), (22,50), (23,50), (24,50), (25,50), (29,50), (30,50), (31,50), (32,50), (32,51), (8,59), (8,60), (8,61), (8,62), (8,63), (8,64), (8,65), (9,59), (9,60), (9,61), (9,62), (9,63), (9,64), (9,65), (37,66), (37,67)],
}, [])

dPeriodNormalAreaExceptions = appenddict({
iPeriodMing : [(99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50)],
})

### Broader Area ###

dBroaderArea = CivDict({
iEgypt :		((60, 26), 	(74, 38)),
iBabylonia :	((72, 37), 	(78, 44)),
iHarappa :		((90, 40), 	(90, 40)),
iChina :		((95, 38), 	(108, 50)),
iGreece :		((62, 39), 	(77, 47)),
iIndia :		((85, 28), 	(99, 43)),
iPhoenicia :	((71, 39), 	(74, 41)),
iPolynesia :	((1, 15), 	(17, 38)),
iPersia :		((70, 37), 	(87, 49)),
iRome :			((49, 35), 	(73, 50)),
iMaya :			((19, 30), 	(26, 37)),
iTamils :		((90, 28), 	(93, 34)),
iEthiopia :		((67, 21), 	(77, 30)),
iKorea :		((106, 45), (110, 52)),
iByzantium :	((58, 34), 	(74, 45)),
iJapan :		((110, 40), (116, 56)),
iVikings :		((58, 56), 	(71, 65)),
iTurks :		((79, 44),	(103, 52)),
iArabia :		((64, 30), 	(85, 44)),
iTibet :		((92, 41), 	(98, 45)),
iIndonesia :	((98, 24), 	(113, 31)),
iMoors :		((51, 37), 	(58, 43)),
iSpain :		((49, 38), 	(55, 46)),
iFrance :		((49, 44), 	(61, 52)),
iKhmer :		((97, 25), 	(105, 39)),
iEngland :		((48, 53), 	(54, 60)),
iHolyRome :		((58, 43), 	(64, 54)),
iRussia :		((65, 48), 	(92, 59)),
iMali :			((48, 26), 	(59, 34)),
iPoland :		((63, 50), 	(67, 55)),
iPortugal :		((49, 40), 	(51, 45)),
iInca :			((24, 14), 	(30, 27)),
iItaly :		((57, 47), 	(65, 47)),
iMongols :		((82, 44), 	(110, 62)),
iAztecs :		((14, 32), 	(24, 43)),
iMughals :		((86, 37), 	(94, 43)),
iOttomans :		((68, 42), 	(86, 49)),
iThailand :		((97, 25), 	(105, 39)),
iCongo :		((61, 19), 	(65, 22)),
iNetherlands :	((56, 51), 	(58, 54)),
iGermany :		((55, 46), 	(67, 57)),
iAmerica :		((10, 42), 	(37, 56)),
iArgentina :	((29,  3), 	(36, 15)),
iColombia :		((33, 32),	(33, 32)),
iBrazil :		((32, 14), 	(43, 28)),
iCanada :		(( 8, 50), 	(37, 67)),
})

dPeriodBroaderArea = {
iPeriodByzantineConstantinople :	((64, 38),	(74, 45)),
iPeriodAustria :					((61, 46),	(66, 50)),
iPeriodPakistan :					((84, 37),	(94, 43)),
}

### Respawn area ###

dRespawnArea = CivDict({
iEgypt :	((65, 30),	(71, 38)),
iChina :	((99, 39),	(107, 47)),
iIndia :	((88, 33),	(96, 41)),
iByzantium :((65, 40),	(69, 46)),
iTurks :	((81, 41),	(86, 48)),
iMoors :	((48, 34),	(58, 39)),
iInca :		((25, 16),	(33, 25)),
iMughals :	((85, 37),	(88, 43)),
})