from Core import *
from RFCUtils import *
from Locations import *
from Events import events, handler


dEvacuatePeriods = {
	iPhoenicia : iPeriodCarthage,
}

dPeriods600AD = {
	iPhoenicia : iPeriodCarthage,
}

dPeriods1700AD = {
	iChina : iPeriodMing,
	iIndia : iPeriodMaratha,
	iDravidia : iPeriodVijayanagara,
	iVikings : iPeriodDenmark,
	iTurks : iPeriodUzbeks,
	iMoors : iPeriodMorocco,
	iSpain : iPeriodSpain,
	iHolyRome : iPeriodAustria,
	iInca : iPeriodPeru,
	iOttomans : iPeriodOttomanConstantinople,
}


dPeriodNames = {
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


@handler("GameStart")
def setup():
	iScenario = scenario()
	
	if iScenario >= i600AD:
		for iCiv, iPeriod in dPeriods600AD.items():
			setPeriod(iCiv, iPeriod)
	
	if iScenario == i1700AD:
		for iCiv, iPeriod in dPeriods1700AD.items():
			setPeriod(iCiv, iPeriod)


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
	
	if iCiv == iArabia:
		setPeriod(iArabia, iPeriodSaudi)
		
	if iCiv == iMongols:
		setPeriod(iCiv, -1)


@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	iCiv = civ(iPlayer)
	iOwnerCiv = civ(iOwner)

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
			

@handler("capitalMoved")
def onCapitalMoved(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)
	
	if iOwnerCiv == iPhoenicia:
		if city.getRegionID() in lEurope + lAfrica:
			setPeriod(iPhoenicia, iPeriodCarthage)
		else:
			setPeriod(iPhoenicia, -1)
	
	if iOwnerCiv == iVikings:
		if player(iOwner).getCurrentEra() >= iRenaissance:
			setPeriod(iVikings, getVikingPeriod(iOwner))
	
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
	
	if iCiv == iVikings:
		if iEra == iRenaissance:
			setPeriod(iVikings, getVikingPeriod(iPlayer))
	
	if iCiv == iMoors:
		if iEra == iIndustrial:
			if player(iPlayer).getCapitalCity().getRegionID() != rIberia:
				setPeriod(iMoors, iPeriodMorocco)

	if iCiv == iSpain:
		if iEra == iRenaissance and player(iCiv).getPeriod() == -1:
			if player(iMoors).isExisting() and cities.owner(iMoors).region(rIberia).none():
				setPeriod(iSpain, iPeriodSpain)
				setPeriod(iMoors, iPeriodMorocco)
	
	if iCiv == iJapan:
		if iEra == iIndustrial:
			setPeriod(iJapan, iPeriodMeiji)
	
	if iCiv == iInca:
		if player(iCiv).getPeriod() == -1:
			if iEra == iRenaissance:
				setPeriod(iInca, iPeriodLateInca)
	
	if iCiv == iItaly:
		if iEra == iIndustrial:
			setPeriod(iItaly, iPeriodModernItaly)
	
	if iPlayer == iGermany:
		if iEra == iDigital:
			setPeriod(iGermany, iPeriodModernGermany)
			
			
def getVikingPeriod(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	
	if capital:
		if isCurrentCapital(iPlayer, "Oslo", "Nidaros"):
			return iPeriodNorway
		elif isCurrentCapital(iPlayer, "Roskilde"):
			return iPeriodDenmark
	
	return -1