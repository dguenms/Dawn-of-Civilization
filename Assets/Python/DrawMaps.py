import os
import csv

from PIL import Image
from pathlib import Path


iWorldX = 150
iWorldY = 80

iNumCivs = 57
(iAmerica, iArabia, iArgentina, iAztecs, iBabylonia, iBrazil, iByzantium, iCanada, iPhoenicia, iCelts, 
iChina, iColombia, iEgypt, iEngland, iEthiopia, iFrance, iGermany, iGreece, iHarappa, iHolyRome, 
iInca, iIndia, iIndonesia, iIran, iItaly, iJapan, iKhmer, iCongo, iKorea, iMali, 
iMaya, iMexico, iMongols, iMoors, iMughals, iNativeAmericans, iNetherlands, iOttomans, iPersia, iPoland, 
iPolynesia, iPortugal, iRome, iRussia, iSpain, iSumeria, iTamils, iThailand, iTibet, iTurks,
iVikings, iZulu, iIndependent, iIndependent2, iNative, iMinor, iBarbarian) = range(iNumCivs)


dCivNames = {
	iAmerica: "America",
	iArabia: "Arabia",
	iArgentina: "Argentina",
	iAztecs: "Aztecs",
	iBabylonia: "Babylonia",
	iBrazil: "Brazil",
	iByzantium: "Byzantium",
	iCanada: "Canada",
	iPhoenicia: "Phoenicia",
	iChina: "China",
	iColombia: "Colombia",
	iEgypt: "Egypt",
	iEngland: "England",
	iEthiopia: "Ethiopia",
	iFrance: "France",
	iGermany: "Germany",
	iGreece: "Greece",
	iHarappa: "Harappa",
	iHolyRome: "Holy_Rome",
	iInca: "Inca",
	iIndia: "India",
	iIndonesia: "Indonesia",
	iIran: "Iran",
	iItaly: "Italy",
	iJapan: "Japan",
	iKhmer: "Khmer",
	iCongo: "Congo",
	iKorea: "Korea",
	iMali: "Mali",
	iMaya: "Maya",
	iMexico: "Mexico",
	iMongols: "Mongolia",
	iMoors: "Moors",
	iMughals: "Mughals",
	iNetherlands: "Netherlands",
	iOttomans: "Turkey",
	iPersia: "Persia",
	iPoland: "Poland",
	iPolynesia: "Polynesia",
	iPortugal: "Portugal",
	iRome: "Rome",
	iRussia: "Russia",
	iSpain: "Spain",
	iTamils: "Tamils",
	iThailand: "Thailand",
	iTibet: "Tibet",
	iTurks: "Turkestan",
	iVikings: "Vikings",
}


(LAND, WATER, PEAK, CORE, HISTORICAL, CONQUEST, FOREIGN) = range(7)

plot_colors = {
	LAND: (175, 175, 175),
	WATER: (50, 100, 100),
	PEAK: (50, 50, 50),
	CORE: (41, 249, 255),
	HISTORICAL: (8, 179, 69),
	CONQUEST: (250, 184, 56),
	FOREIGN: (240, 64, 102),
}


dCoreArea = {
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
}

dCoreAreaExceptions = {
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
}


def iterate_map(file_path):
	full_file_path = Path.cwd() / "Assets/Maps" / file_path
	
	with open(full_file_path) as file:
		for y, line in enumerate(csv.reader(file)):
			for x, value in enumerate(line):
				if not value:
					yield (x, y), 0
				else:
					yield (x, y), int(value)


def is_core(iCiv, tile):
	x, y = tile
	
	(tBLx, tBLy), (tTRx, tTRy) = dCoreArea[iCiv]
	lExceptions = dCoreAreaExceptions.get(iCiv, [])
	
	return tBLx <= x <= tTRx and tBLy <= y <= tTRy and (x, y) not in lExceptions


def iterate_plot_types(iCiv):
	civ_name = dCivNames[iCiv]

	settler_values = iterate_map(f"Settler/{civ_name}.csv")
	war_values = iterate_map(f"War/{civ_name}.csv")
	terrain_values = iterate_map("Export/BaseTerrain.csv")
	
	for ((x, y), iSettlerValue), (_, iWarValue), (_, iTerrainValue) in zip(settler_values, war_values, terrain_values):
		if iTerrainValue == 2:
			yield (x, y), PEAK
			
		elif iTerrainValue != 0 and is_core(iCiv, (x, iWorldY-1-y)):
			yield (x, y), CORE
		
		elif iSettlerValue > 0:
			yield (x, y), HISTORICAL
		
		elif iWarValue > 1:
			yield (x, y), CONQUEST
		
		elif iTerrainValue == 0:
			yield (x, y), WATER
		
		else:
			yield (x, y), LAND


def draw_stability_map(iCiv):
	civ_name = dCivNames[iCiv]

	image = Image.new("RGB", (iWorldX, iWorldY), "white")
	pixels = image.load()

	for (x, y), plot_type in iterate_plot_types(iCiv):
		pixels[x, y] = plot_colors[plot_type]
	
	image = image.resize((iWorldX * 4, iWorldY * 4))
	
	image_path = Path.cwd() / "Maps" / f"{civ_name}.png"
	image.save(image_path)


def draw_stability_maps():
	for iCiv in dCivNames:
		draw_stability_map(iCiv)


if __name__ == "__main__":
	draw_stability_maps()