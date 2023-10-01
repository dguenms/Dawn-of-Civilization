from Consts import *

# Peak that change to hills during the game, like Bogota
lPeakExceptions = [(31, 13), (32, 19), (27, 29), (88, 47), (40, 66)]
	
### Capitals ###

dCapitals = CivDict({
iEgypt :		(79, 43), # Memphis
iBabylonia :	(89, 47), # Babylon
iHarappa :		(102, 47), # Harappa
iAssyria :		(89, 50), # Ash-shur
iChina :		(121, 52), # Chang'an
iHittites :		(83, 54), # Hattusha
iGreece :		(76, 51), # Athens
iIndia :		(110, 45), # Pataliputra
iPhoenicia :	(84, 47), # Tyre
iNubia :		(81, 38), # Meroe
iPolynesia :	(4, 21), # Tonga
iPersia :		(94, 45), # Persepolis
iRome :			(68, 53), # Rome
iCelts :		(62, 57), # Nemessos
iMaya :			(22, 41), # Tikal
iTamils :		(107, 34), # Thanjavur
iEthiopia :		(84, 35), # Aksum
iVietnam : 		(121, 42), # Hanoi
iToltecs :		(17, 43), # Tollan
iKushans :		(100, 52), # Bactra
iKorea :		(131, 54), # Seoul
iByzantium :	(79, 55), # Constantinople
iMalays :		(120, 27), # Palembang
iJapan :		(137, 53), # Kyoto
iVikings :		(67, 75), # Nidaros
iTurks :		(105, 58), # Orduqent
iArabia :		(86, 39), # Mecca
iTibet :		(113, 48), # Lhasa
iMoors :		(57, 49), # Cordoba
iJava :			(126, 25), # Trowulan
iSpain :		(57, 51), # Madrid
iFrance :		(61, 60), # Paris
iKhmer :		(121, 37), # Angkor
iEngland :		(58, 64), # London
iHolyRome :		(65, 62), # Cologne
iBurma :		(117, 42), # Bagan
iRus :			(81, 62), # Kyiv
iMali :			(58, 35), # Djenne
iPoland :		(74, 61), # Krakow
iPortugal :		(54, 50), # Lisboa
iInca :			(31, 24), # Cuzco
iItaly :		(67, 55), # Florence
iMongols :		(119, 61), # Karakorum
iAztecs :		(17, 43), # Tenochtitlan
iMughals : 		(105, 46), # Delhi
iRussia :		(85, 66), # Moscow
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
iAssyria :		((88, 49),	(90, 51)),
iChina :		((120, 51),	(126, 56)),
iHittites :		((82, 52),	(85, 54)),
iGreece :		((74, 49),	(80, 53)),
iIndia :		((107, 44),	(111, 46)),
iPhoenicia :	((84, 47),	(85, 49)),
iNubia :		((78, 38),	(81, 39)),
iPolynesia :	((3, 20),	(5, 23)),
iPersia :		((92, 43),	(95, 50)),
iRome :			((66, 50),	(72, 57)),
iCelts :		((59, 56),	(63, 61)),
iMaya :			((21, 41),	(23, 44)),
iTamils :		((105, 31),	(108, 35)),
iEthiopia :		((82, 33),	(85, 36)),
iVietnam :		((120, 41),	(122, 43)),
iToltecs :		((16, 42),	(18, 44)),
iKushans :		((100, 49),	(102, 53)),
iKorea :		((130, 53),	(132, 56)),
iByzantium :	((76, 51),	(87, 55)),
iMalays :		((119, 26),	(121, 31)),
iJapan :		((135, 52),	(140, 55)),
iVikings :		((65, 67),	(68, 75)),
iTurks :		((96, 54),	(107, 59)),
iArabia :		((84, 38),	(90, 49)),
iTibet :		((111, 47),	(114, 49)),
iMoors :		((56, 44),	(61, 50)),
iJava :			((119, 24), (128, 28)),
iSpain :		((54, 51),	(59, 54)),
iFrance :		((59, 56),	(63, 62)),
iKhmer :		((120, 34),	(123, 38)),
iEngland :		((56, 63),	(59, 67)),
iHolyRome :		((64, 59),	(70, 63)),
iBurma :		((116, 38),	(117, 43)),
iRus :			((80, 61),	(82, 69)),
iMali :			((57, 34),	(61, 38)),
iPoland :		((72, 61),	(76, 64)),
iPortugal :		((54, 50),	(55, 52)),
iInca :			((28, 22),	(32, 24)),
iItaly :		((65, 54),	(70, 57)),
iMongols :		((116, 57),	(126, 66)),
iAztecs :		((16, 41),	(19, 44)),
iMughals :		((100, 45),	(107, 49)),
iRussia :		((81, 65),	(90, 70)),
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
iToltecs :  [(17, 42), (18, 42)],
iByzantium :[(76, 51), (84, 51), (85, 51), (86, 51), (86, 52), (87, 51), (87, 52)],
iTurks :	[(105, 54), (105, 55), (106, 54), (106, 55), (107, 54), (107, 55), (107, 56)],
iArabia :	[(88, 38), (88, 39), (88, 40), (88, 41), (88, 42), (88, 43), (88, 44), (89, 38), (89, 39), (89, 40), (89, 41), (89, 42), (89, 43), (89, 44), (90, 38), (90, 39), (90, 40), (90, 41), (90, 42), (90, 43), (90, 44)],
iMoors :	[(60, 44), (61, 44), (61, 45)],
iJava :		[(124, 28), (125, 28), (126, 28), (127, 28)],
iSpain :	[(54, 51), (54, 52), (55, 51), (55, 52)],
iFrance :	[(61, 56), (62, 56), (62, 62), (63, 56), (63, 62)],
iKhmer :	[(123, 37), (123, 38)],
iHolyRome :	[(64, 59), (64, 60), (69, 59), (70, 59), (70, 60), (70, 63)],
iMali :		[(57, 38), (60, 34), (61, 34), (61, 35)],
iPoland :	[(72, 61)],
iMongols :	[(116, 57), (116, 58), (116, 65), (116, 66), (117, 57), (117, 58), (117, 65), (117, 66), (122, 65), (122, 66), (123, 57), (123, 65), (123, 66), (124, 57), (124, 65), (124, 66), (125, 57), (125, 64), (125, 65), (125, 66), (126, 57), (126, 63), (126, 64), (126, 65), (126, 66)],
iRussia :	[(81, 65), (82, 65), (83, 65), (84, 69), (84, 70), (85, 69), (85, 70), (86, 69), (86, 70), (87, 69), (87, 70), (88, 69), (88, 70), (89, 69), (89, 70), (90, 65), (90, 69), (90, 70)],
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

### Expansion area ###

# TODO: only set expansion to true or false and use war maps
dExpansionArea = CivDict({
# iPersia :		((69, 37), (78, 45)),
# iRome :			((51, 38), (73, 48)),
# iVikings :		((48, 50), (56, 60)),
# iTurks :		((69, 36), (85, 45)),
# iArabia :		((50, 36), (85, 43)),
# iSpain :		((49, 40), (55, 45)),
# iMongols :		((72, 37), (110, 56)),
# iMughals :		((86, 33), (96, 40)),
# iOttomans :		((64, 32), (77, 48)),
})

dExpansionAreaExceptions = CivDict({
}, [])

### Respawn area ###

dRespawnArea = CivDict({
iEgypt :	((76, 39),	(83, 45)),
iChina :	((117, 43),	(129, 58)),
iIndia :	((103, 37),	(110, 46)),
iByzantium :((76, 51),	(87, 55)),
iTurks :	((92, 48),	(101, 55)),
iMoors :	((56, 43),	(61, 47)),
iInca :		((27, 21),	(32, 28)),
iMughals :	((99, 42),	(104, 50)),
iOttomans : ((78, 51),	(87, 55)),
})

dRespawnAreaExceptions = CivDict({
iEgypt :	[(83, 43), (83, 44), (83, 45)],
iChina :	[(117, 43), (117, 44), (117, 45), (117, 46), (117, 49), (117, 50), (117, 51), (117, 52), (117, 53), (117, 54), (117, 55), (117, 56), (117, 57), (117, 58), (118, 43), (118, 44), (118, 56), (118, 57), (118, 58), (119, 43), (119, 57), (119, 58), (120, 43), (120, 57), (120, 58), (121, 43), (122, 43)],
iIndia :	[(103, 43), (103, 44), (103, 45), (103, 46), (104, 46)],
iByzantium :[(76, 51), (84, 51), (85, 51), (86, 51), (86, 52), (87, 51), (87, 52)],
iTurks :	[(99, 48), (99, 49), (100, 48), (100, 49), (100, 50), (101, 48), (101, 49), (101, 50)],
iMughals :	[(102, 42), (102, 43), (102, 44), (102, 45), (103, 42), (103, 43), (103, 44), (103, 45), (104, 42), (104, 43), (104, 44), (104, 45)],
}, [])