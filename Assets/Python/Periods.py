from Core import *
from RFCUtils import *
from Locations import *

from Events import events, handler
from DynamicCivs import isCurrentCapital


dEvacuatePeriods = {
	iPhoenicia : iPeriodCarthage,
}

dPeriods3000BC = {
	iEgypt : iPeriodOldKingdom,
}

dPeriods600AD = {
	iPhoenicia : iPeriodCarthage,
	iCelts : iPeriodInsularCelts,
}

dPeriods1700AD = {
	iChina : iPeriodMing,
	iIndia : iPeriodMaratha,
	iCelts : iPeriodInsularCelts,
	iDravidia : iPeriodVijayanagara,
	iNorse : iPeriodDenmark,
	iTurks : iPeriodUzbeks,
	iMoors : iPeriodMorocco,
	iSpain : iPeriodSpain,
	iHolyRome : iPeriodAustria,
	iEngland : iPeriodUnitedKingdom,
	iInca : iPeriodPeru,
	iOttomans : iPeriodOttomanConstantinople,
}

dScenarioPeriods = {
	-3000: dPeriods3000BC,
	600: dPeriods600AD,
	1700: dPeriods1700AD,
}


dPeriodNames = {
	# Egypt
	iPeriodOldKingdom:				"Old_Kingdom",
	iPeriodMiddleKingdom:			"Middle_Kingdom",
	iPeriodPtolemaicEgypt:			"Ptolemaic_Egypt",

	iPeriodMing:					"Ming",
	iPeriodMaratha:					"Maratha",
	iPeriodModernGreece:			"Modern_Greece",
	iPeriodCarthage:				"Carthage",
	iPeriodInsularCelts:			"Insular_Celts",
	iPeriodVijayanagara:			"Vijayanagara",
	iPeriodByzantineConstantinople:	"Byzantine_Constantinople",
	iPeriodSeljuks:					"Seljuks",
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


def setPeriod(iCiv, iPeriod):
	if game.getPeriod(iCiv) == iPeriod:
		return

	game.setPeriod(iCiv, iPeriod)
	
	events.fireEvent("periodChange", iCiv, iPeriod)
	
	iPlayer = slot(iCiv)
	if iPlayer >= 0:
		events.fireEvent("playerPeriodChange", iPlayer, iPeriod)


def evacuate(iPlayer):
	if player(iPlayer).getPeriod() == -1:
		iCiv = civ(iPlayer)
		if iCiv in dEvacuatePeriods:
			setPeriod(iCiv, dEvacuatePeriods[iCiv])
			
			if cities.core(iPlayer).owner(iPlayer) > 0:
				return True
			else:
				setPeriod(iCiv, -1)
	return False


@handler("birth")
def onBirth(iPlayer):
	iCiv = civ(iPlayer)
	if iCiv == iFrance:
		setPeriod(iCelts, iPeriodInsularCelts)
	elif iCiv == iGermany:
		setPeriod(iHolyRome, iPeriodAustria)


@handler("collapse")
def onCollapse(iPlayer):
	if civ(iPlayer) == iChina:
		setPeriod(iMongols, iPeriodYuan)


@handler("resurrection")
def onResurrection(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iGreece:
		setPeriod(iGreece, iPeriodModernGreece)
	
	if iCiv == iChina:
		if year() > year(dBirth[iMongols]):
			setPeriod(iChina, iPeriodMing)
	
	if iCiv == iIndia:
		if year() < year(1900):
			setPeriod(iIndia, iPeriodMaratha)
		else:
			setPeriod(iIndia, -1)
	
	if iCiv == iCelts:
		setPeriod(iCelts, iPeriodInsularCelts)
	
	if iCiv == iArabia:
		setPeriod(iArabia, iPeriodSaudi)
		
	if iCiv == iMongols:
		setPeriod(iCiv, -1)


@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	iCiv = civ(iPlayer)
	iOwnerCiv = civ(iOwner)

	# Egypt
	if iOwnerCiv == iIndependent:
		if iCiv == iEgypt:
			setPeriod(iEgypt, iPeriodMiddleKingdom)
	
	if iOwnerCiv == iBarbarian:
		if iCiv == iEgypt:
			setPeriod(iEgypt, iPeriodNewKingdom)

	if iOwnerCiv == iEgypt:
		if iCiv in [iGreece, iRome]:
			setPeriod(iEgypt, iPeriodPtolemaicEgypt)

	if iCiv == iSpain:
		if not cities.owner(iMoors).region(rIberia):
			setPeriod(iSpain, iPeriodSpain)
	
	if iCiv == iEngland:
		if player(iPlayer).getCurrentEra() == iIndustrial and city in cities.regions(rBritain, rIreland) and cities.regions(rBritain, rIreland).all(lambda city: city.getOwner() == iPlayer):
			setPeriod(iEngland, iPeriodGreatBritain)
		elif player(iPlayer).getCurrentEra() >= iRenaissance and city in cities.region(rBritain) and cities.region(rBritain).all(lambda city: city.getOwner() == iPlayer):
			setPeriod(iEngland, iPeriodUnitedKingdom)

	if iCiv == iOttomans:
		if city.at(*tConstantinople):
			setPeriod(iOttomans, iPeriodOttomanConstantinople)
	
	if iTurks in [iCiv, iOwnerCiv]:
		if isControlled(iTurks, plots.core(iIran)):
			setPeriod(iTurks, iPeriodSeljuks)
		else:
			setPeriod(iTurks, -1)

	if iOwnerCiv == iByzantium:
		if bConquest and player(iByzantium).getNumCities() <= 4:
			setPeriod(iByzantium, iPeriodByzantineConstantinople)
	
	if iOwnerCiv == iCelts:
		if player(iCelts).getNumCities() > 0 and cities.core(iCelts).owner(iCelts).count() == 0:
			setPeriod(iCelts, iPeriodInsularCelts)
	
	if iOwnerCiv == iMoors:
		if not cities.owner(iMoors).region(rIberia):
			setPeriod(iMoors, iPeriodMorocco)

	
@handler("firstCity")
def onCityBuilt(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)

	if iOwnerCiv == iPhoenicia:
		if city.getRegionID in lEurope + lAfrica:
			setPeriod(iPhoenicia, iPeriodCarthage)


@handler("vassalState")
def onVassalState(iMaster, iVassal, bVassal, bCapitulated):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)
	
	if bVassal:
		if iVassalCiv == iInca:
			setPeriod(iInca, iPeriodPeru)
		
		if iVassalCiv == iChina:
			if bCapitulated and iMasterCiv == iMongols:
				setPeriod(iMongols, iPeriodYuan)
		
		if iVassalCiv == iEgypt:
			if iMasterCiv in [iGreece, iRome]:
				setPeriod(iEgypt, iPeriodPtolemaicEgypt)
			

@handler("capitalMoved")
def onCapitalMoved(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)
	
	if iOwnerCiv == iPhoenicia:
		if city.getRegionID() in lEurope + lAfrica:
			setPeriod(iPhoenicia, iPeriodCarthage)
		else:
			setPeriod(iPhoenicia, -1)
	
	if iOwnerCiv == iNorse:
		if player(iOwner).getCurrentEra() >= iRenaissance:
			setPeriod(iNorse, getNorsePeriod(iOwner))
	
	if iOwnerCiv == iMoors:
		if player(iOwner).getCurrentEra() >= iIndustrial and city.getRegionID() != rIberia:
			setPeriod(iMoors, iPeriodMorocco)


@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	iCiv = civ(iPlayer)
	iEra = infos.tech(iTech).getEra()
	
	if iCiv == iDravidia:
		if iEra == iMedieval:
			setPeriod(iDravidia, iPeriodVijayanagara)
	
	if iCiv == iNorse:
		if iEra == iRenaissance:
			setPeriod(iNorse, getNorsePeriod(iPlayer))
	
	if iCiv == iMoors:
		if iEra == iIndustrial:
			if player(iPlayer).getCapitalCity().getRegionID() != rIberia:
				setPeriod(iMoors, iPeriodMorocco)

	if iCiv == iJapan:
		if iEra == iIndustrial:
			setPeriod(iJapan, iPeriodMeiji)
	
	if iCiv == iEngland:
		if iEra == iRenaissance:
			if cities.region(rBritain).all(lambda city: city.getOwner() == iPlayer):
				setPeriod(iEngland, iPeriodUnitedKingdom)
		
		elif iEra == iIndustrial:
			if cities.regions(rBritain, rIreland).all(lambda city: city.getOwner() == iPlayer):
				setPeriod(iEngland, iPeriodGreatBritain)
		
		elif iEra == iGlobal:
			if player(iPlayer).getPeriod() == iPeriodGreatBritain:
				setPeriod(iEngland, iPeriodUnitedKingdom)
	
	if iCiv == iInca:
		if player(iPlayer).getPeriod() == -1:
			if iEra == iRenaissance:
				setPeriod(iInca, iPeriodLateInca)
	
	if iCiv == iItaly:
		if iEra == iIndustrial:
			setPeriod(iItaly, iPeriodModernItaly)
	
	if iPlayer == iGermany:
		if iEra == iDigital:
			setPeriod(iGermany, iPeriodModernGermany)
			
			
def getNorsePeriod(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	
	if capital:
		if isCurrentCapital(iPlayer, "Oslo", u"Niðaróss"):
			return iPeriodNorway
		elif isCurrentCapital(iPlayer, "Roskilde"):
			return iPeriodDenmark
	
	return -1