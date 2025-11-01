import os
import csv

from PIL import Image
from pathlib import Path


def Civ(x):
	return x


class CivDict:
	
	def __init__(self, dict, default=None):
		self.dict = dict
		self.default = default
	
	def __getitem__(self, key):
		if self.default is None:
			return self.dict[key]
		
		return self.dict.get(key, self.default)
	
	def __contains__(self, key):
		return key in self.dict
	
	def get(self, key, default=None):
		return self.dict.get(key, default)


def appenddict(dict):
	return CivDict(dict, [])


iWorldX = 150
iWorldY = 80

iNumCivs = 68
(iAmerica, iArabia, iArgentina, iAssyria, iAztecs, iBabylonia, iBrazil, iBurma, iByzantium, iCanada, 
iCarthage, iCelts, iChina, iColombia, iDravidia, iEgypt, iEngland, iEthiopia, iFrance, iGermany, 
iGreece, iHarappa, iHittites, iHolyRome, iInca, iIndia, iIran, iItaly, iJapan, iJava, 
iKhmer, iCongo, iKorea, iKushans, iMalays, iMali, iMaya, iMexico, iMongols, iMoors, 
iMughals, iNativeAmericans, iNetherlands, iNorse, iNubia, iOttomans, iPersia, iPoland, iPolynesia, iPortugal, 
iRome, iRus, iRussia, iSpain, iSumeria, iSwahili, iSweden, iThailand, iTibet, iToltecs, 
iTurks, iVietnam, iZulu, iIndependent, iIndependent2, iNative, iMinor, iBarbarian) = tuple(Civ(i) for i in range(iNumCivs))

iNumPeriods = 28
(iPeriodPtolemaicEgypt, iPeriodMakuria, iPeriodMing, iPeriodMaratha, iPeriodModernGreece, 
iPeriodCarthage, iPeriodInsularCelts, iPeriodVijayanagara, iPeriodByzantineConstantinople, iPeriodSeljuks,
iPeriodNationalFrance, iPeriodMeiji, iPeriodDenmark, iPeriodNorway, iPeriodUzbeks, 
iPeriodSaudi, iPeriodMorocco, iPeriodSpain, iPeriodAustria, iPeriodUnitedKingdom, 
iPeriodGreatBritain, iPeriodYuan, iPeriodPeru, iPeriodLateInca, iPeriodModernItaly, 
iPeriodPakistan, iPeriodOttomanConstantinople, iPeriodModernGermany) = range(iNumPeriods)

iNumRegions = 85
(rBritain, rIreland, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland,
rBaltics, rScandinavia, rRuthenia, rPonticSteppe, rEuropeanArctic, rUrals, rAnatolia, rCaucasus, rLevant, rMesopotamia,
rArabia, rEgypt, rNubia, rMaghreb, rPersia, rKhorasan, rTransoxiana, rSindh, rPunjab, rRajputana,
rHindustan, rBengal, rDeccan, rDravida, rIndochina, rIndonesia, rPhilippines, rSouthChina, rNorthChina, rKorea,
rJapan, rTibet, rTarimBasin, rMongolia, rManchuria, rAmur, rCentralAsianSteppe, rSiberia, rAustralia, rOceania,
rEthiopia, rHornOfAfrica, rSwahiliCoast, rGreatLakes, rZambezi, rMadagascar, rCape, rKalahari, rCongo, rGuinea, 
rSahel, rSahara, rAtlanticSeaboard, rDeepSouth, rMidwest, rGreatPlains, rAridoamerica, rCalifornia, rCascadia, rOntario, 
rQuebec, rMaritimes, rAmericanArctic, rCaribbean, rMesoamerica, rCentralAmerica, rNewGranada, rAndes, rAmazonia, rBrazil, 
rSouthernCone, rAntarctica, rHinduKush, rRussia, rVolga) = range(iNumRegions)

iNumReligions = 10
(iJudaism, iOrthodoxy, iCatholicism, iProtestantism, iIslam, iHinduism, iBuddhism, iConfucianism, iTaoism, iZoroastrianism) = range(iNumReligions)

iNumReligionMapTypes = 5
(iNone, iMinority, iPeriphery, iHistorical, iCore) = range(iNumReligionMapTypes)

iPhoenicia = iCarthage


dCivNames = {
	iAmerica: "America",
	iArabia: "Arabia",
	iArgentina: "Argentina",
	iAssyria: "Assyria",
	iAztecs: "Aztecs",
	iBabylonia: "Babylonia",
	iBrazil: "Brazil",
	iByzantium: "Byzantium",
	iCanada: "Canada",
	iCarthage: "Phoenicia",
	iCelts: "Celts",
	iChina: "China",
	iColombia: "Colombia",
	iDravidia: "Dravidia",
	iEgypt: "Egypt",
	iEngland: "England",
	iEthiopia: "Ethiopia",
	iFrance: "France",
	iGermany: "Germany",
	iGreece: "Greece",
	iHarappa: "Harappa",
	iHittites: "Hittites",
	iHolyRome: "Holy_Rome",
	iInca: "Inca",
	iIndia: "India",
	iIran: "Iran",
	iItaly: "Italy",
	iJapan: "Japan",
	iJava: "Java",
	iKhmer: "Khmer",
	iCongo: "Congo",
	iKorea: "Korea",
	iKushans: "Kushans",
	iMali: "Mali",
	iMaya: "Maya",
	iMexico: "Mexico",
	iMongols: "Mongolia",
	iMoors: "Moors",
	iMughals: "Mughals",
	iNetherlands: "Netherlands",
	iNorse: "Norse",
	iNubia: "Nubia",
	iOttomans: "Turkey",
	iPersia: "Persia",
	iPoland: "Poland",
	iPolynesia: "Polynesia",
	iPortugal: "Portugal",
	iRome: "Rome",
	iRus: "Ruthenia",
	iRussia: "Russia",
	iSpain: "Spain",
	iSwahili: "Swahili",
	iSweden: "Sweden",
	iThailand: "Thailand",
	iTibet: "Tibet",
	iToltecs: "Toltecs",
	iTurks: "Turkestan",
	iVietnam: "Vietnam",
}

dCivPeriods = {
	iEgypt: [iPeriodPtolemaicEgypt],
	iNubia: [iPeriodMakuria],
	iChina: [iPeriodMing],
	iIndia: [iPeriodMaratha],
	iGreece: [iPeriodModernGreece],
	iCarthage: [iPeriodCarthage],
	iCelts: [iPeriodInsularCelts],
	iDravidia: [iPeriodVijayanagara],
	iByzantium: [iPeriodByzantineConstantinople],
	iTurks: [iPeriodSeljuks, iPeriodUzbeks],
	iFrance: [iPeriodNationalFrance],
	iJapan: [iPeriodMeiji],
	iNorse: [iPeriodDenmark, iPeriodNorway],
	iArabia: [iPeriodSaudi],
	iMoors: [iPeriodMorocco],
	iSpain: [iPeriodSpain],
	iHolyRome: [iPeriodAustria],
	iEngland: [iPeriodUnitedKingdom, iPeriodGreatBritain],
	iMongols: [iPeriodYuan],
	iInca: [iPeriodPeru, iPeriodLateInca],
	iItaly: [iPeriodModernItaly],
	iMughals: [iPeriodPakistan],
	iOttomans: [iPeriodOttomanConstantinople],
	iGermany: [iPeriodModernGermany],
}

dPeriodNames = {
	iPeriodPtolemaicEgypt:			"Ptolemaic_Egypt",
	iPeriodMakuria:					"Makuria",
	iPeriodMing:					"Ming",
	iPeriodMaratha:					"Maratha",
	iPeriodModernGreece:			"Modern_Greece",
	iPeriodCarthage:				"Carthage",
	iPeriodInsularCelts:			"Insular_Celts",
	iPeriodVijayanagara:			"Vijayanagara",
	iPeriodByzantineConstantinople:	"Byzantine_Constantinople",
	iPeriodSeljuks:					"Seljuks",
	iPeriodNationalFrance:			"National_France",
	iPeriodMeiji:					"Meiji",
	iPeriodDenmark:					"Denmark",
	iPeriodNorway:					"Norway",
	iPeriodUzbeks:					"Uzbeks",
	iPeriodSaudi:					"Saudi",
	iPeriodMorocco:					"Morocco",
	iPeriodSpain:					"Spain",
	iPeriodAustria:					"Austria",
	iPeriodUnitedKingdom:			"United_Kingdom",
	iPeriodGreatBritain:			"Great_Britain",
	iPeriodYuan:					"Yuan",
	iPeriodPeru:					"Peru",
	iPeriodLateInca:				"Late_Inca",
	iPeriodModernItaly:				"Modern_Italy",
	iPeriodPakistan:				"Pakistan",
	iPeriodOttomanConstantinople:	"Ottoman_Constantinople",
	iPeriodModernGermany:			"Modern_Germany",
}

dReligionNames = {
	iJudaism: "Judaism",
	iOrthodoxy: "Orthodoxy",
	iCatholicism: "Catholicism",
	iProtestantism: "Protestantism",
	iIslam: "Islam",
	iHinduism: "Hinduism",
	iBuddhism: "Buddhism",
	iConfucianism: "Confucianism",
	iTaoism: "Taoism",
	iZoroastrianism: "Zoroastrianism",
}


(LAND, WATER, PEAK, CORE, HISTORICAL, CONQUEST, FOREIGN, MINORITY, PERIPHERY) = range(9)

plot_colors = {
	LAND: (175, 175, 175),
	WATER: (50, 100, 100),
	PEAK: (50, 50, 50),
	CORE: (41, 249, 255),
	HISTORICAL: (8, 179, 69),
	CONQUEST: (250, 184, 56),
	FOREIGN: (240, 64, 102),
	PERIPHERY: (250, 184, 56),
	MINORITY: (255, 220, 115),
}


dCoreArea = CivDict({
iEgypt :		((78, 41),	(80, 44)),
iBabylonia :	((88, 45),	(90, 48)),
iHarappa :		((101, 46),	(102, 47)),
iAssyria :		((88, 49),	(90, 51)),
iNubia :		((80, 37),	(81, 39)),
iChina :		((120, 51),	(126, 56)),
iHittites :		((82, 52),	(85, 54)),
iGreece :		((74, 49),	(80, 53)),
iIndia :		((107, 44),	(111, 46)),
iPhoenicia :	((84, 47),	(85, 49)),
iPolynesia :	((3, 20),	(5, 23)),
iPersia :		((92, 43),	(95, 50)),
iRome :			((66, 50),	(72, 57)),
iCelts :		((59, 56),	(63, 61)),
iMaya :			((21, 41),	(23, 44)),
iDravidia :		((105, 31),	(108, 35)),
iEthiopia :		((82, 33),	(85, 36)),
iVietnam :		((120, 41),	(122, 43)),
iToltecs :		((16, 42),	(18, 44)),
iKushans :		((100, 46),	(104, 53)),
iKorea :		((130, 53),	(132, 56)),
iKhmer :		((120, 36),	(122, 38)),
iByzantium :	((74, 49),	(81, 55)),
iFrance :		((59, 58),	(63, 62)),
iMalays :		((119, 26),	(121, 31)),
iJapan :		((135, 52),	(140, 55)),
iNorse :		((65, 67),	(68, 75)),
iTurks :		((96, 54),	(107, 59)),
iArabia :		((84, 39),	(90, 48)),
iTibet :		((111, 47),	(114, 49)),
iMoors :		((56, 44),	(61, 50)),
iJava :			((125, 24),	(128, 25)),
iSpain :		((54, 51),	(59, 54)),
iEngland :		((56, 63),	(59, 67)),
iHolyRome :		((64, 59),	(70, 63)),
iBurma :		((116, 38),	(117, 43)),
iRus :			((80, 61),	(82, 69)),
iSwahili :		((83, 19),	(85, 27)),
iMali :			((57, 34),	(61, 38)),
iPoland :		((72, 61),	(76, 64)),
iPortugal :		((54, 50),	(55, 52)),
iInca :			((28, 22),	(32, 24)),
iItaly :		((65, 54),	(70, 57)),
iMongols :		((116, 57),	(126, 66)),
iAztecs :		((16, 41),	(19, 44)),
iMughals :		((102, 45),	(107, 48)),
iThailand :		((118, 34),	(120, 39)),
iSweden :		((71, 69),	(73, 73)),
iRussia :		((81, 65),	(90, 70)),
iOttomans :		((79, 51),	(84, 55)),
iCongo :		((71, 24),	(74, 27)),
iIran:			((91, 48),	(94, 52)),
iNetherlands :	((62, 63),	(63, 65)),
iGermany :		((65, 62),	(76, 66)),
iAmerica :		((25, 54),	(32, 58)),
iArgentina :	((35, 13),	(38, 16)),
iMexico :		((14, 41),	(19, 44)),
iColombia :		((26, 34),	(35, 38)),
iBrazil :		((42, 19),	(47, 25)),
iCanada :		((26, 59),	(37, 62)),
})

dCoreAreaExceptions = CivDict({
iEgypt :	[(80, 43), (80, 44)],
iBabylonia: [(88, 45)],
iHarappa :	[(102, 46)],
iChina :	[(120, 54), (120, 55), (120, 56), (121, 54), (121, 55), (121, 56), (126, 51)],
iGreece :	[(74, 53), (80, 53)],
iPhoenicia :[(85, 47)],
iPersia :	[(94, 48), (94, 49), (94, 50), (95, 46), (95, 47), (95, 48), (95, 49), (95, 50)],
iRome :		[(66, 51), (66, 52), (70, 57), (71, 56), (71, 57), (72, 55), (72, 56), (72, 57)],
iToltecs :  [(17, 42), (18, 42)],
iKushans :	[(103, 46), (103, 52), (103, 53), (104, 46), (104, 47), (104, 50), (104, 51), (104, 52), (104, 53)],
iKhmer :	[(120, 36)],
iTurks :	[(105, 54), (105, 55), (106, 54), (106, 55), (107, 54), (107, 55), (107, 56)],
iFrance :	[(62, 58), (62, 62), (63, 58), (63, 62)],
iArabia :	[(88, 39), (88, 40), (88, 41), (88, 42), (88, 43), (88, 44), (89, 39), (89, 40), (89, 41), (89, 42), (89, 43), (89, 44), (90, 39), (90, 40), (90, 41), (90, 42), (90, 43), (90, 44)],
iMoors :	[(60, 44), (61, 44), (61, 45)],
iSpain :	[(54, 51), (54, 52), (55, 51), (55, 52)],
iHolyRome :	[(64, 59), (64, 60), (69, 59), (70, 59), (70, 60), (70, 63)],
iSwahili :	[(83, 20), (83, 21), (83, 22), (83, 23), (83, 27)],
iMali :		[(57, 38), (60, 34), (61, 34), (61, 35)],
iPoland :	[(72, 61)],
iMongols :	[(116, 57), (116, 58), (116, 65), (116, 66), (117, 57), (117, 58), (117, 65), (117, 66), (122, 65), (122, 66), (123, 57), (123, 65), (123, 66), (124, 57), (124, 65), (124, 66), (125, 57), (125, 64), (125, 65), (125, 66), (126, 57), (126, 63), (126, 64), (126, 65), (126, 66)],
iAztecs :	[(19, 41)],
iThailand :	[(118, 39)],
iRussia :	[(81, 65), (82, 65), (83, 65), (84, 69), (84, 70), (85, 69), (85, 70), (86, 69), (86, 70), (87, 69), (87, 70), (88, 69), (88, 70), (89, 69), (89, 70), (90, 65), (90, 69), (90, 70)],
iOttomans :	[(79, 55), (83, 51), (84, 51), (84, 52)],
iCongo :	[(71, 26), (71, 27), (72, 27)],
iIran :		[(91, 48)],
iGermany :	[(72, 64), (73, 62), (73, 63), (73, 64), (74, 62), (74, 63), (74, 64), (75, 62), (75, 63), (75, 64), (76, 62), (76, 63), (76, 64)],
iAmerica :	[(25, 54), (26, 54)],
iColombia :	[(26, 36), (27, 37), (31, 34), (31, 35), (32, 34), (32, 35), (33, 34), (33, 35), (34, 34), (34, 35), (35, 34), (35, 35)],
iCanada :	[(26, 62), (27, 62), (28, 62), (29, 62), (30, 59), (30, 62), (31, 59), (32, 59), (33, 59), (33, 60)],
}, [])

dPeriodCoreArea = {
iPeriodMakuria :					((78, 37),	(80, 39)),
iPeriodMing : 						((120, 49),	(129, 56)),
iPeriodModernGreece :				((74, 49),	(76, 54)),
iPeriodMaratha : 					((102, 38),	(107, 47)),
iPeriodCarthage:					((64, 45),	(70, 48)),
iPeriodInsularCelts :				((52, 64),	(56, 67)),
iPeriodByzantineConstantinople :	((77, 54),	(80, 55)),
iPeriodNationalFrance :				((59, 56),	(63, 62)),
iPeriodMeiji : 						((134, 49),	(140, 59)),
iPeriodSeljuks : 					((92, 48),	(98, 53)),
iPeriodSaudi :						((84, 38),	(90, 43)),
iPeriodMorocco : 					((56, 43),	(60, 47)),
iPeriodSpain : 						((54, 48),	(59, 54)),
iPeriodAustria : 					((69, 58),	(72, 61)),
iPeriodUnitedKingdom : 				((56, 63),	(59, 70)),
iPeriodGreatBritain :				((53, 62),	(59, 70)),
iPeriodLateInca :					((28, 20),	(34, 25)),
iPeriodModernItaly : 				((65, 53),	(70, 57)),
iPeriodYuan : 						((117, 56),	(127, 62)),
iPeriodPakistan : 					((100, 46),	(103, 49)),
iPeriodOttomanConstantinople : 		((77, 50),	(84, 55)),
iPeriodModernGermany : 				((65, 61),	(69, 65)),
}

dPeriodCoreAreaExceptions = appenddict({
iPeriodMakuria :				[(78, 37)],
iPeriodMing :					[(120, 49), (120, 50), (120, 54), (120, 55), (120, 56), (121, 49), (121, 50), (121, 54), (121, 55), (121, 56), (122, 49), (122, 50), (123, 49), (123, 50), (128, 56)],
iPeriodModernGreece :			[(74, 54)],
iPeriodMaratha :				[(102, 43), (102, 44), (102, 45), (102, 46), (102, 47), (103, 43), (103, 44), (103, 45), (103, 46), (103, 47), (106, 38), (106, 39), (106, 40), (107, 38), (107, 39), (107, 40)],
iPeriodCarthage :				[(64, 45), (64, 46), (65, 45), (65, 46), (70, 48)],
iPeriodNationalFrance :			[(61, 56), (62, 56), (62, 62), (63, 56), (63, 62)],
iPeriodSpain :					[(54, 49), (54, 50), (54, 51), (54, 52), (55, 49), (55, 50), (55, 51), (55, 52)],
iPeriodGreatBritain :			[(53, 65), (53, 66), (53, 67), (55, 70)],
iPeriodLateInca :				[(34, 24), (34, 25)],
iPeriodModernItaly :			[(65, 53)],
iPeriodOttomanConstantinople :	[(83, 51), (84, 51), (84, 52)],
iPeriodModernGermany :			[(69, 61)],
})

tSpreadFactors = (
# Judaism
{
	iMinority :	[rBritain, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland, rRuthenia, rLevant, rMesopotamia, rAnatolia, rCaucasus, rArabia, rEgypt, rMaghreb, rPersia, rEthiopia, rAtlanticSeaboard, rMidwest, rCalifornia, rOntario, rQuebec, rMaritimes]
},
# Orthodoxy
{
	iCore :		[rRuthenia, rRussia, rEthiopia, rGreece, rCaucasus],
	iHistorical : 	[rBalkans, rAnatolia, rLevant, rMesopotamia, rEgypt, rNubia, rEuropeanArctic, rUrals, rSiberia],
	iPeriphery : 	[rMaghreb, rItaly, rVolga, rPonticSteppe, rAmericanArctic, rCentralAsianSteppe],
	iMinority :	[rBaltics, rPoland, rPersia, rKhorasan, rTransoxiana, rTarimBasin, rNorthChina],
},
# Catholicism
{
	iCore :		[rFrance, rCentralEurope, rPoland, rIreland, rItaly, rIberia],
	iHistorical :	[rBritain, rLowerGermany, rQuebec, rMaritimes, rAtlanticSeaboard, rCaribbean, rAridoamerica, rMesoamerica, rCentralAmerica, rNewGranada, rAndes, rAmazonia, rBrazil, rSouthernCone, rCongo, rKalahari, rCape, rPhilippines],
	iPeriphery :	[rBalkans, rGreece, rRuthenia, rAmericanArctic, rOntario, rMidwest, rDeepSouth, rGreatPlains, rCalifornia, rAustralia, rOceania, rGuinea, rSwahiliCoast, rMadagascar],
},
# Protestantism
{
	iCore :		[rBritain, rLowerGermany, rScandinavia, rAtlanticSeaboard, rMidwest, rOntario, rGreatPlains, rDeepSouth, rMaritimes],
	iHistorical :	[rBaltics, rCalifornia, rCascadia, rAmericanArctic, rAustralia],
	iPeriphery :	[rFrance, rOceania, rCape, rZambezi, rSwahiliCoast],
	iMinority : 	[rPoland, rCentralEurope, rBrazil, rKorea]
},
# Islam
{
	iCore : 	[rArabia, rMesopotamia, rEgypt, rLevant],
	iHistorical : 	[rPersia, rKhorasan, rSindh, rPunjab, rTransoxiana, rMaghreb, rIndonesia, rSahel, rSahara, rHornOfAfrica, rVolga],
	iPeriphery : 	[rNubia, rIberia, rAnatolia, rBalkans, rHinduKush, rHindustan, rRajputana, rBengal, rDeccan, rPonticSteppe, rCentralAsianSteppe, rSwahiliCoast],
	iMinority : 	[rUrals, rSiberia, rCaucasus, rTarimBasin, rMongolia],
},
# Hinduism
{
	iCore : 	[rHindustan, rRajputana, rDeccan, rBengal, rDravida],
	iHistorical : 	[rPunjab, rSindh, rIndochina, rIndonesia, rPhilippines],
},
# Buddhism
{
	iCore : 	[rHindustan, rRajputana, rBengal, rTibet, rIndochina],
	iHistorical : 	[rDeccan, rDravida, rPunjab, rSindh, rHinduKush, rTarimBasin, rMongolia, rNorthChina, rSouthChina, rKorea, rJapan, rIndonesia, rKhorasan],
	iMinority :	[rTransoxiana, rKhorasan],
},
# Confucianism
{
	iCore : 	[rNorthChina, rSouthChina, rManchuria],
	iHistorical :	[rKorea],
	iPeriphery : 	[rMongolia, rTibet],
	iMinority : 	[rJapan, rIndonesia, rIndochina, rAustralia],
},
# Taoism
{
	iCore : 	[rNorthChina, rSouthChina],
	iHistorical : 	[rManchuria],
	iPeriphery : 	[rTibet, rMongolia],
},
# Zoroastrianism
{
	iCore :		[rPersia],
	iPeriphery : 	[rKhorasan, rMesopotamia, rTransoxiana, rLevant],
	iMinority : 	[rSindh, rRajputana],
},
)


def get_full_path(path):
	return Path.cwd() / "Assets/Maps" / path


def map_exists(file_path):
	try:
		open(get_full_path(file_path))
	except IOError:
		return False
	
	return True


def iterate_map(file_path):
	full_file_path = get_full_path(file_path)
	
	with open(full_file_path) as file:
		for y, line in enumerate(csv.reader(file)):
			for x, value in enumerate(line):
				if not value:
					yield (x, y), 0
				else:
					yield (x, y), int(value)
					
					
def is_area(rectangle, exceptions, identifier, tile):
	x, y = tile
	
	(x1, y1), (x2, y2) = rectangle[identifier]
	excluded = exceptions.get(identifier, [])
	
	return x1 <= x <= x2 and y1 <= y <= y2 and (x, y) not in excluded


def is_core(iCiv, tile):
	return is_area(dCoreArea, dCoreAreaExceptions, iCiv, tile)


def is_period_core(identifier, tile):
	iCiv, iPeriod = identifier
	
	if iPeriod not in dPeriodCoreArea:
		return is_core(iCiv, tile)
	
	return is_area(dPeriodCoreArea, dPeriodCoreAreaExceptions, iPeriod, tile)


def iterate_civ_map(iCiv):
	civ_name = dCivNames[iCiv]

	settler_values = iterate_map(f"Settler/{civ_name}.csv")
	war_values = iterate_map(f"War/{civ_name}.csv")
	
	return iterate_plot_types(iCiv, settler_values, war_values, is_core)


def iterate_period_map(iCiv, iPeriod):
	period_name = dPeriodNames[iPeriod]
	civ_name = dCivNames[iCiv]
	
	settler_map = f"Settler/Period/{period_name}.csv"
	war_map = f"War/Period/{period_name}.csv"
	
	if map_exists(settler_map):
		settler_values = iterate_map(settler_map)
	else:
		settler_values = iterate_map(f"Settler/{civ_name}.csv")
	
	if map_exists(war_map):
		war_values = iterate_map(war_map)
	else:
		war_values = iterate_map(f"War/{civ_name}.csv")
	
	if iPeriod in dPeriodCoreArea:
		core_func = is_period_core
		identifier = (iCiv, iPeriod)
	else:
		core_func = is_core
		identifier = iCiv
	
	return iterate_plot_types(identifier, settler_values, war_values, core_func)


def iterate_plot_types(identifier, settler_values, war_values, core_func):
	terrain_values = iterate_map("Export/BaseTerrain.csv")
	
	for ((x, y), iSettlerValue), (_, iWarValue), (_, iTerrainValue) in zip(settler_values, war_values, terrain_values):
		if iTerrainValue == 2:
			yield (x, y), PEAK
			
		elif iTerrainValue != 0 and core_func(identifier, (x, iWorldY-1-y)):
			yield (x, y), CORE
		
		elif iSettlerValue > 0:
			yield (x, y), HISTORICAL
		
		elif iWarValue > 1:
			yield (x, y), CONQUEST
		
		elif iTerrainValue == 0:
			yield (x, y), WATER
		
		else:
			yield (x, y), LAND


def draw_stability_map(name, values):
	print(name)
	
	image = Image.new("RGB", (iWorldX, iWorldY), "white")
	pixels = image.load()

	for (x, y), plot_type in values:
		pixels[x, y] = plot_colors[plot_type]
	
	image = image.resize((iWorldX * 4, iWorldY * 4))
	
	image_path = Path.cwd() / "Maps" / f"{name}.png"
	image.save(image_path)


def draw_stability_map_for_civ(iCiv):
	civ_name = dCivNames[iCiv]
	values = iterate_civ_map(iCiv)
	
	draw_stability_map(civ_name, values)


def draw_stability_map_for_period(iCiv, iPeriod):
	civ_name = dCivNames[iCiv]
	period_name = dPeriodNames[iPeriod]
	values = iterate_period_map(iCiv, iPeriod)
	
	draw_stability_map(f"Periods/{civ_name}_{period_name}", values)


def should_draw_for_period(iPeriod):
	period_name = dPeriodNames[iPeriod]
	
	return map_exists(f"Settler/Period/{period_name}.csv") or map_exists(f"War/Period/{period_name}.csv") or iPeriod in dPeriodCoreArea


def getSpreadFactor(iReligion, iRegion):
	if iRegion < 0: 
		return -1
	
	return next((iFactor for iFactor, lRegions in tSpreadFactors[iReligion].items() if iRegion in lRegions), iNone)


def iterate_religion_spread_factors(iReligion):
	region_values = iterate_map("Regions.csv")
	terrain_values = iterate_map("Export/BaseTerrain.csv")
	
	for ((x, y), iRegion), (_, iTerrain) in zip(region_values, terrain_values):
		iSpreadFactor = getSpreadFactor(iReligion, iRegion)
	
		if iTerrain == 0:
			yield (x, y), WATER
	
		elif iTerrain == 2:
			yield (x, y), PEAK
		
		elif iSpreadFactor == iCore:
			yield (x, y), CORE
		
		elif iSpreadFactor == iHistorical:
			yield (x, y), HISTORICAL
		
		elif iSpreadFactor == iPeriphery:
			yield (x, y), PERIPHERY
		
		elif iSpreadFactor == iMinority:
			yield (x, y), MINORITY
		
		else:
			yield (x, y), LAND
			


def draw_religion_map(iReligion):
	print(dReligionNames[iReligion])
	
	image = Image.new("RGB", (iWorldX, iWorldY), "white")
	pixels = image.load()
	
	for (x, y), spread_factor_type in iterate_religion_spread_factors(iReligion):
		pixels[x, y] = plot_colors[spread_factor_type]
	
	image = image.resize((iWorldX * 4, iWorldY * 4))
	
	image_path = Path.cwd() / "Maps/Religions" / f"{dReligionNames[iReligion]}.png"
	image.save(image_path)


def draw_maps():
	for iCiv in dCivNames:
		draw_stability_map_for_civ(iCiv)
		
		for iPeriod in dCivPeriods.get(iCiv, []):
			if should_draw_for_period(iPeriod):
				draw_stability_map_for_period(iCiv, iPeriod)
	
	for iReligion in range(iNumReligions):
		draw_religion_map(iReligion)


if __name__ == "__main__":
	draw_maps()