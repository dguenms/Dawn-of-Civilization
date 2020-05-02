from Core import *
from RFCUtils import *
from Events import handler

import Setup as init
import SettlerMaps as settler
import WarMaps as war


dEvacuatePeriods = {
	iPhoenicia : iPeriodCarthage,
	iKhmer : iPeriodVietnam,
}


def setPeriod(iCiv, iPeriod):
	if not player(iCiv).isAlive():
		return

	player(iCiv).setPeriod(iPeriod)
	
	iPlayer = slot(iCiv)
	init.updateCore(iPlayer)
	settler.updateMap(iPlayer)
	war.updateMap(iPlayer)


def evacuate(iPlayer):
	if player(iPlayer).getPeriod() == -1:
		iCiv = civ(iPlayer)
		if iCiv in dEvacuatePeriods:
			setPeriod(iCiv, dEvacuatePeriods[iCiv])
			
			if getOwnedCoreCities(iPlayer) > 0:
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
		tTL, tBR = dCoreArea[iPersia]
		if isAreaControlled(slot(iTurks), tTL, tBR):
			setPeriod(iTurks, iPeriodSeljuks)
		else:
			setPeriod(iTurks, -1)
			
	if iOwnerCiv == iByzantium:
		if bConquest and player(iByzantium).getNumCities() <= 4:
			setPeriod(iByzantium, iPeriodByzantineConstantinople)
	
	
def onCityBuilt(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)

	if iOwnerCiv == iPhoenicia:
		if city.at(58, 39) and getOwnedCoreCities(iOwner) > 0:
			setPeriod(iPhoenicia, iPeriodCarthage)


def onVassalState(iMaster, iVassal, bCapitulated):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)

	if iVassalCiv == iInca:
		setPeriod(iInca, iPeriodPeru)
		
	if iVassalCiv == iChina:
		if bCapitulated and iMasterCiv == iMongols:
			setPeriod(iMongols, iPeriodYuan)
			

def onPalaceMoved(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)
	
	if iOwnerCiv == iPhoenicia:
		if city.at(58, 39):
			setPeriod(iPhoenicia, iPeriodCarthage)


def onTechAcquired(iPlayer, iEra):
	iCiv = civ(iPlayer)

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