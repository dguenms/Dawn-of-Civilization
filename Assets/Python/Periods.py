from Core import *
from RFCUtils import *
from Events import events, handler


dEvacuatePeriods = {
	iPhoenicia : iPeriodCarthage,
	iKhmer : iPeriodVietnam,
}


def setPeriod(iCiv, iPeriod):
	if not player(iCiv).isAlive():
		return
		
	if player(iCiv).getPeriod() == iPeriod:
		return

	player(iCiv).setPeriod(iPeriod)
	
	iPlayer = slot(iCiv)
	events.fireEvent("periodChange", iPlayer, iPeriod)


def evacuate(iPlayer):
	if player(iPlayer).getPeriod() == -1:
		iCiv = civ(iPlayer)
		if iCiv in dEvacuatePeriods:
			setPeriod(iCiv, dEvacuatePeriods[iCiv])
			
			if cities.core(iPlayer).owner(iPlayer) > 0:
				return True
			else:
				setPeriod(iPlayer, -1)
	return False


def setup():
	iScenario = scenario()
	
	if iScenario == i1700AD:
		setPeriod(iIndia, iPeriodMaratha)
		setPeriod(iKhmer, iPeriodVietnam)
		setPeriod(iMoors, iPeriodMorocco)
		setPeriod(iSpain, iPeriodSpain)
		setPeriod(iHolyRome, iPeriodAustria)
		setPeriod(iOttomans, iPeriodOttomanConstantinople)


def onBirth(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iThailand:
		setPeriod(iKhmer, iPeriodVietnam)
	
	if iCiv == iGermany:
		setPeriod(iHolyRome, iPeriodAustria)


def onCollapse(iPlayer):
	if civ(iPlayer) == iChina:
		setPeriod(iMongols, iPeriodYuan)


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
		
	# TODO: it was like this in onResurrection - figure out the intent
	if iCiv in [iArabia, iMongols]:
		setPeriod(iCiv, -1)


@handler("cityAcquired")
def onCityAcquired(iOwner, iPlayer, city, bConquest):
	iCiv = civ(iPlayer)
	iOwnerCiv = civ(iOwner)

	if iCiv == iOttomans:
		if city.at(68, 45):
			setPeriod(iOttomans, iPeriodOttomanConstantinople)
	
	if iTurks in [iCiv, iOwnerCiv]:
		if isControlled(iTurks, plots.core(iPersia)):
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
		if player(iOwner).getCurrentEra() >= iRenaissance and player(iOwner).getPeriod() == -1:
			setPeriod(iVikings, getVikingPeriod(iOwner))
	
	if iOwnerCiv == iMoors:
		if player(iOwner).getCurrentEra() >= iIndustrial and city.getRegionID() != iIberia:
			setPeriod(iMoors, iPeriodMorocco)


@handler("techAcquired")
def onTechAcquired(iTech, iTeam, iPlayer):
	iCiv = civ(iPlayer)
	iEra = infos.tech(iTech).getEra()
	
	if iCiv == iVikings:
		if iEra == iRenaissance:
			setPeriod(iVikings, getVikingPeriod(iPlayer))
	
	if iCiv == iMoors:
		if iEra == iIndustrial:
			if player(iPlayer).getCapitalCity().getRegionID() != rIberia:
				setPeriod(iMoors, iPeriodMorocco)

	if iCiv == iSpain:
		if iEra == iRenaissance and player(iCiv).getPeriod() == -1:
			if player(iMoors).isAlive() and cities.owner(iMoors).region(rIberia).none():
				setPeriod(iSpain, iPeriodSpain)
				setPeriod(iMoors, iPeriodMorocco)
	
	if iCiv == iJapan:
		if iEra == iIndustrial:
			setPeriod(iJapan, iPeriodMeiji)
	
	if iCiv == iItaly:
		if iEra == iIndustrial:
			setPeriod(iItaly, iPeriodModernItaly)
	
	if iPlayer == iGermany:
		if iEra == iDigital:
			setPeriod(iGermany, iPeriodModernGermany)
			
			
def getVikingPeriod(iPlayer):
	capital = player(iPlayer).getCapitalCity()
	
	if capital:
		if isCurrentCapital(iPlayer, "Stockholm", "Kalmar"):
			return iPeriodSweden
		elif isCurrentCapital(iPlayer, "Oslo", "Nidaros"):
			return iPeriodNorway
		elif isCurrentCapital(iPlayer, "Roskilde"):
			return iPeriodDenmark
	
	return -1