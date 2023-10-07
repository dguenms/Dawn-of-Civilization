from Core import *

import Modifiers as NewModifiers
import OldModifiers


lOldCivilizations = [
	iEgypt,
	iBabylonia,
	iHarappa,
	iChina,
	iGreece,
	iIndia,
	iPhoenicia,
	iPolynesia,
	iPersia,
	iRome,
	iMaya,
	iTamils,
	iEthiopia,
	iKorea,
	iByzantium,
	iJapan,
	iVikings,
	iTurks,
	iArabia,
	iTibet,
	iMalays, # Indonesia
	iMoors,
	iSpain,
	iFrance,
	iKhmer,
	iEngland,
	iHolyRome,
	iRussia,
	iMali,
	iPoland,
	iPortugal,
	iInca,
	iItaly,
	iMongols,
	iAztecs,
	iMughals,
	iOttomans,
	iThailand,
	iCongo,
	iIran,
	iNetherlands,
	iGermany,
	iAmerica,
	iArgentina,
	iMexico,
	iColombia,
	iBrazil,
	iCanada,
]


def compare(iOldIndex, iNewIndex, iCivilization):
	tOldModifiers = tuple(tModifier[iOldIndex] for tModifier in OldModifiers.tModifiers)
	tNewModifiers = tuple(tModifier[iNewIndex] for tModifier in NewModifiers.tModifiers)
	
	if tOldModifiers != tNewModifiers:
		print "Different modifiers for %s: old [%d] %s - new [%d] %s" % (infos.civ(iCivilization).getText(), iOldIndex, tOldModifiers, iNewIndex, tNewModifiers)
	

def compareAll():
	for iOldIndex, iCivilization in enumerate(lOldCivilizations):
		iNewIndex = lBirthOrder.index(iCivilization)
		compare(iOldIndex, iNewIndex, iCivilization)