from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]
	
### Capitals ###

dCapitals = CivDict({
iEgypt :		(79, 43), # Memphis
iBabylonia :	(89, 47), # Babylon
iHarappa :		(102, 47), # Harappa
iChina :		(121, 52), # Chang'an
iGreece :		(76, 51), # Athens
iIndia :		(110, 45), # Pataliputra
iPhoenicia :	(84, 47), # Tyre
iPolynesia :	(4, 21), # Tonga
iPersia :		(94, 45), # Persepolis
iRome :			(68, 53), # Rome
iMaya :			(22, 41), # Tikal
iTamils :		(107, 34), # Thanjavur
iEthiopia :		(84, 35), # Aksum
iKorea :		(131, 54), # Seoul
iByzantium :	(79, 55), # Constantinople
iJapan :		(137, 53), # Kyoto
iVikings :		(67, 75), # Nidaros
iTurks :		(105, 58), # Orduqent
iArabia :		(86, 39), # Mecca
iTibet :		(113, 48), # Lhasa
iIndonesia :	(120, 27), # Palembang
iMoors :		(57, 49), # Cordoba
iSpain :		(57, 51), # Madrid
iFrance :		(61, 60), # Paris
iKhmer :		(121, 37), # Angkor
iEngland :		(58, 64), # London
iHolyRome :		(65, 62), # Cologne
iRussia :		(86, 66), # Moskow
iMali :			(58, 35), # Djenne
iPoland :		(74, 61), # Krakow
iPortugal :		(54, 50), # Lisboa
iInca :			(31, 24), # Cuzco
iItaly :		(67, 55), # Florence
iMongols :		(119, 61), # Karakorum
iAztecs :		(17, 43), # Tenochtitlan
iMughals : 		(105, 46), # Delhi
iOttomans : 	(80, 53), # Sogut
iThailand : 	(119, 37), # Ayutthaya
iCongo : 		(71, 25), # Mbanza Kongo
iIran : 		(93, 48), # Esfahan
iNetherlands :	(62, 64), # Amsterdam
iGermany : 		(69, 63), # Berlin
iAmerica :		(29, 54), # Washington
iArgentina :	(38, 13), # Buenos Aires
iMexico :		(17, 43), # Mexico City
iColombia :		(30, 34), # Bogota
iBrazil :		(44, 20), # Rio de Janeiro
iCanada :		(32, 61), # Montreal
})

dPeriodCapitals = {
iPeriodMing :			(125, 56), # Beijing
iPeriodMaratha :		(105, 46),	# Delhi
iPeriodCarthage : 		(67, 48),	# Carthage
iPeriodVijayanagara :	(106, 37),	# Vijayanagara
iPeriodVietnam :		(121, 42),	# Ha Noi
iPeriodAustria :		(71, 59),	# Vienna
}

# new capital locations if changed during the game
dNewCapitals = CivDict({
iJapan :	(140, 54),	# Tokyo
iVikings :	(73, 71),	# Stockholm
iHolyRome :	(71, 59),	# Vienna
iItaly :	(68, 53),	# Rome
iMongols :	(125, 56),	# Khanbaliq
iOttomans :	(79, 55),	# Istanbul
})

# new capital locations on respawn
dRespawnCapitals = CivDict({
iEgypt :	(79, 43),	# Cairo
iChina :	(125, 56),	# Beijing
iIndia :	(105, 46),	# Delhi
iPersia :	(93, 48),	# Esfahan
iEthiopia :	(84, 32),	# Addis Ababa
iJapan :	(140, 54),	# Tokyo
iVikings :	(73, 71),	# Stockholm
iTurks : 	(97, 49),	# Herat
iIndonesia :(123, 25),	# Jakarta
iMoors :	(57, 44),	# Marrakesh
iHolyRome :	(71, 59),	# Vienna
iInca :		(28, 25),	# Lima
iItaly :	(68, 53),	# Rome
iMughals :	(99, 43),	# Karachi
iOttomans :	(79, 55),	# Istanbul
})

### Birth Area ###

# TODO: core area is fallback, define actual birth areas where different
dBirthArea = CivDict({
})

# TODO: restore and adjust
dExtendedBirthArea = CivDict({
# iPersia :	((74, 37), 	(85, 44)), 	# includes Assyria and Anatolia
# iSpain : 	((49, 43), 	(55, 46)), 	# includes Catalonia
# iInca : 	((26, 19), 	(31, 24)),
# iMongols : 	((81, 45), 	(105, 54)), # 6 more west, 1 more south
# iOttomans : ((67, 41), 	(76, 48)), 	# 2 more west
# iArgentina :((29, 3), 	(35, 13)), 	# includes Chile
})

# TODO: core area is fallback, define actual birth areas where different
dBirthAreaExceptions = CivDict({
}, [])

### Core Area ###

dCoreArea = CivDict({
iEgypt :		((78, 41),	(80, 44)),
iBabylonia :	((88, 45),	(90, 48)),
iHarappa :		((99, 45),	(102, 47)),
iChina :		((120, 51),	(126, 56)),
iGreece :		((74, 49),	(80, 53)),
iIndia :		((107, 44),	(111, 46)),
iPhoenicia :	((84, 47),	(85, 49)),
iPolynesia :	((3, 20),	(5, 23)),
iPersia :		((92, 43),	(95, 50)),
iRome :			((66, 50),	(72, 57)),
iMaya :			((21, 41),	(23, 44)),
iTamils :		((105, 31),	(108, 35)),
iEthiopia :		((82, 33),	(85, 36)),
iKorea :		((130, 53),	(132, 56)),
iByzantium :	((76, 51),	(87, 55)),
iJapan :		((135, 52),	(140, 55)),
iVikings :		((65, 67),	(68, 75)),
iTurks :		((96, 54),	(107, 59)),
iArabia :		((84, 38),	(90, 49)),
iTibet :		((111, 47),	(114, 49)),
iIndonesia :	((119, 24),	(128, 28)),
iMoors :		((56, 44),	(61, 50)),
iSpain :		((54, 51),	(59, 54)),
iFrance :		((59, 56),	(63, 62)),
iKhmer :		((120, 34),	(123, 38)),
iEngland :		((56, 63),	(59, 67)),
iHolyRome :		((64, 59),	(70, 63)),
iRussia :		((81, 65),	(90, 70)),
iMali :			((57, 34),	(61, 38)),
iPoland :		((72, 61),	(76, 64)),
iPortugal :		((54, 50),	(55, 52)),
iInca :			((28, 22),	(32, 24)),
iItaly :		((65, 54),	(70, 57)),
iMongols :		((116, 57),	(126, 66)),
iAztecs :		((16, 41),	(19, 44)),
iMughals :		((100, 45),	(107, 49)),
iOttomans :		((79, 51),	(87, 55)),
iThailand :		((118, 34),	(120, 39)),
iCongo :		((71, 24),	(74, 27)),
iIran:			((91, 48),	(94, 52)),
iNetherlands :	((62, 63),	(63, 65)),
iGermany :		((65, 62),	(76, 66)),
iAmerica :		((24, 54),	(33, 59)),
iArgentina :	((35, 13),	(38, 16)),
iMexico :		((14, 41),	(19, 44)),
iColombia :		((28, 34),	(30, 38)),
iBrazil :		((42, 19),	(47, 25)),
iCanada :		((26, 59),	(37, 62)),
})

dCoreAreaExceptions = CivDict({
iEgypt :	[(80, 43), (80, 44)],
iBabylonia: [(88, 45)],
iHarappa :	[(99, 46), (99, 47), (101, 45), (102, 45), (102, 46)],
iChina :	[(120, 54), (120, 55), (120, 56), (121, 54), (121, 55), (121, 56), (126, 51)],
iGreece :	[(74, 53), (80, 53)],
iPhoenicia :[(85, 47)],
iPersia :	[(94, 48), (94, 49), (94, 50), (95, 46), (95, 47), (95, 48), (95, 49), (95, 50)],
iRome :		[(66, 51), (66, 52), (70, 57), (71, 56), (71, 57), (72, 55), (72, 56), (72, 57)],
iByzantium :[(76, 51), (84, 51), (85, 51), (86, 51), (86, 52), (87, 51), (87, 52)],
iTurks :	[(105, 54), (105, 55), (106, 54), (106, 55), (107, 54), (107, 55), (107, 56)],
iArabia :	[(88, 38), (88, 39), (88, 40), (88, 41), (88, 42), (88, 43), (88, 44), (89, 38), (89, 39), (89, 40), (89, 41), (89, 42), (89, 43), (89, 44), (90, 38), (90, 39), (90, 40), (90, 41), (90, 42), (90, 43), (90, 44)],
iIndonesia :[(124, 28), (125, 28), (126, 28), (127, 28)],
iMoors :	[(60, 44), (61, 44), (61, 45)],
iSpain :	[(54, 51), (54, 52), (55, 51), (55, 52)],
iFrance :	[(61, 56), (62, 56), (62, 62), (63, 56), (63, 62)],
iKhmer :	[(123, 37), (123, 38)],
iHolyRome :	[(64, 59), (64, 60), (69, 59), (70, 59), (70, 60), (70, 63)],
iRussia :	[(81, 65), (82, 65), (83, 65), (84, 69), (84, 70), (85, 69), (85, 70), (86, 69), (86, 70), (87, 69), (87, 70), (88, 69), (88, 70), (89, 69), (89, 70), (90, 65), (90, 69), (90, 70)],
iMali :		[(57, 38), (60, 34), (61, 34), (61, 35)],
iPoland :	[(72, 61)],
iMongols :	[(116, 57), (116, 58), (116, 65), (116, 66), (117, 57), (117, 58), (117, 65), (117, 66), (122, 65), (122, 66), (123, 57), (123, 65), (123, 66), (124, 57), (124, 65), (124, 66), (125, 57), (125, 64), (125, 65), (125, 66), (126, 57), (126, 63), (126, 64), (126, 65), (126, 66)],
iGermany :	[(58, 52), (58, 53), (58, 54), (61, 49), (61, 50), (62, 49), (62, 50), (62, 51), (63, 49), (63, 50), (63, 51), (64, 49), (64, 50), (64, 51), (64, 52), (64, 53), (65, 49), (65, 51), (65, 52), (65, 53)],
iOttomans :	[(79, 55)],
iThailand :	[(118, 39)],
iCongo :	[(71, 26), (71, 27), (72, 27)],
iIran :		[(91, 48)],
iGermany :	[(72, 64), (73, 62), (73, 63), (73, 64), (74, 62), (74, 63), (74, 64), (75, 62), (75, 63), (75, 64), (76, 62), (76, 63), (76, 64)],
iAmerica :	[(24, 54), (25, 54), (26, 54), (26, 59), (27, 59)],
iCanada :	[(26, 62), (27, 62), (28, 62), (29, 62), (30, 59), (30, 62), (31, 59), (32, 59), (33, 59), (33, 60)],
}, [])

dPeriodCoreArea = {
iPeriodMing : 						((120, 49),	(129, 56)),
iPeriodModernGreece :				((74, 49),	(76, 54)),
iPeriodMaratha : 					((102, 38),	(107, 47)),
iPeriodCarthage:					((64, 45),	(70, 48)),
iPeriodByzantineConstantinople :	((77, 54),	(80, 55)),
iPeriodMeiji : 						((134, 49),	(140, 59)),
iPeriodSeljuks : 					((92, 48),	(98, 53)),
iPeriodSaudi :						((84, 38),	(90, 43)),
iPeriodMorocco : 					((56, 43),	(60, 47)),
iPeriodSpain : 						((54, 48),	(59, 54)),
iPeriodVietnam : 					((120, 40),	(122, 43)),
iPeriodAustria : 					((69, 58),	(72, 61)),
iPeriodLateInca :					((28, 20),	(34, 25)),
iPeriodModernItaly : 				((65, 53),	(70, 57)),
iPeriodYuan : 						((117, 56),	(127, 62)),
iPeriodPakistan : 					((100, 46),	(103, 49)),
iPeriodOttomanConstantinople : 		((77, 50),	(87, 55)),
iPeriodModernGermany : 				((65, 61),	(69, 65)),
}

dPeriodCoreAreaExceptions = appenddict({
iPeriodMing :					[(120, 49), (120, 50), (120, 54), (120, 55), (120, 56), (121, 49), (121, 50), (121, 54), (121, 55), (121, 56), (122, 49), (122, 50), (123, 49), (123, 50), (128, 56)],
iPeriodModernGreece :			[(74, 54)],
iPeriodMaratha :				[(102, 43), (102, 44), (102, 45), (102, 46), (102, 47), (103, 43), (103, 44), (103, 45), (103, 46), (103, 47), (106, 38), (106, 39), (106, 40), (107, 38), (107, 39), (107, 40)],
iPeriodCarthage :				[(64, 45), (64, 46), (65, 45), (65, 46), (70, 48)],
iPeriodSpain :					[(54, 49), (54, 50), (54, 51), (54, 52), (55, 49), (55, 50), (55, 51), (55, 52)],
iPeriodVietnam :				[(120, 40)],
iPeriodLateInca :				[(34, 24), (34, 25)],
iPeriodModernItaly :			[(65, 53)],
iPeriodOttomanConstantinople :	[(86, 50), (87, 50)],
iPeriodModernGermany :			[(69, 61)],
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
iOttomans :		((68, 42), 	(77, 49)),
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
iArabia :	[(81, 38), (82, 38), (82, 37), (72, 30), (72, 31), (72, 32), (73, 30)],
iSpain :	[(49, 44), (49, 43), (49, 42), (49, 41)],
iFrance :	[(51, 46), (52, 46), (53, 46), (58, 47), (58, 46), (58, 51), (58, 52), (57, 52)],
iHolyRome : [(63, 52), (63, 53), (63, 54), (64, 51), (64, 52), (64, 53), (64, 54), (65, 51), (65, 52), (65, 53), (65, 54)],
iRussia :	[(80, 49), (68, 62), (68, 61), (68, 60), (68, 59)],
iPoland :	[(63, 50), (64, 50)],
iItaly :	[(62, 47), (63, 47), (63, 46)],
iMongols :	[(92, 52), (92, 53), (92, 54), (93, 54), (94, 54), (100, 48), (101, 48), (102, 48), (103, 48), (104, 48)],
iAztecs :	[(20, 35)],
iOttomans : [(76, 42), (77, 42), (77, 43), (77, 44)],
iMexico :	[(20, 35)],
iArgentina :[(35, 12), (35, 13), (36, 12), (36, 13), (36, 14), (36, 15)],
iCanada :	[(11,50), (12,50), (13,50), (14,50), (16,50), (17,50), (18,50), (19,50), (20,50), (21,50), (22,50), (23,50), (24,50), (25,50), (29,50), (30,50), (31,50), (32,50), (32,51), (8,59), (8,60), (8,61), (8,62), (8,63), (8,64), (8,65), (9,59), (9,60), (9,61), (9,62), (9,63), (9,64), (9,65), (37,66), (37,67)],
}, [])

dPeriodNormalAreaExceptions = appenddict({
iPeriodMing : 	 [(99, 49), (100, 49), (101, 49), (99, 50), (100, 50), (101, 50), (102, 50)],
iPeriodAustria : [(61, 46), (61, 47)],
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

### Expansion area ###

dExpansionArea = CivDict({
iPersia :		((69, 37), (78, 45)),
iRome :			((51, 38), (73, 48)),
iVikings :		((48, 50), (56, 60)),
iTurks :		((69, 36), (85, 45)),
iArabia :		((50, 36), (85, 43)),
iMongols :		((72, 37), (110, 56)),
iMughals :		((86, 33), (96, 40)),
iOttomans :		((64, 32), (77, 48)),
})

dExpansionAreaExceptions = CivDict({
iRome :		[(62, 48), (63, 48), (64, 48), (65, 48), (68, 48), (72, 48), (64, 47), (65, 47), (66, 47), (67, 47), (65, 46), (66, 46), (65, 45), (51, 38), (53, 38)],
iTurks :	[(69, 36), (70, 36), (71, 36), (69, 39), (71, 40), (73, 36), (74, 36), (75, 36), (76, 36), (77, 36), (78, 36), (74, 37), (75, 37), (76, 37), (77, 37), (78, 37)],
iArabia :	[(53, 37), (54, 37), (55, 37), (56, 37), (57, 37), (53, 36), (54, 36), (55, 36), (56, 36), (57, 36), (58, 36), (59, 36), (60, 36), (58, 42), (58, 43), (61, 43), (62, 43), (65, 43), (65, 42), (66, 42), (67, 42), (67, 41), (65, 40), (66, 40), (69, 43), (70, 43), (71, 43), (72, 43), (73, 43), (74, 43)],
iMongols :	[(74, 37), (75, 37), (76, 37), (77, 37), (78, 37), (84, 37), (85, 37), (86, 37), (87, 37), (88, 37), (89, 37), (90, 37), (91, 37), (92, 37), (93, 37), (94, 37), (95, 37), (98, 37), (99, 37), (100, 37), (101, 37), (85, 38), (86, 38), (87, 38), (88, 38), (89, 38), (90, 38), (91, 38), (92, 38), (93, 38), (94, 38), (95, 38), (96, 38), (97, 38), (98, 38), (99, 38), (100, 38), (101, 38), (102, 38), (86, 39), (87, 39), (88, 39), (89, 39), (90, 39), (91, 39), (92, 39), (93, 39), (94, 39), (95, 39), (96, 39), (86, 40), (87, 40), (88, 40), (89, 40), (90, 40), (91, 40), (92, 40), (93, 40), (94, 40), (95, 40), (96, 40), (87, 41), (88, 41), (89, 41), (90, 41), (91, 41), (92, 41), (87, 42), (88, 42), (89, 42), (90, 42), (88, 43), (89, 43), (88, 44)],
iOttomans :	[(75, 37), (76, 37), (77, 37), (75, 36), (76, 36), (77, 36), (76, 35), (77, 35), (77, 34), (77, 33), (77, 42), (77, 43), (77, 44), (77, 45)],
}, [])

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
iOttomans : ((68, 42), 	(75, 45)),
})