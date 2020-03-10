from Core import *
from RFCUtils import *

import Areas as areas
import SettlerMaps as settler
import WarMaps as war


dEvacuatePeriods = {
	iPhoenicia : iPeriodCarthage,
	iKhmer : iPeriodVietnam,
}


def setPeriod(iPlayer, iPeriod):
	if not player(iPlayer).isAlive():
		return

	player(iPlayer).setPeriod(iPeriod)
	
	areas.updateCore(iPlayer)
	settler.updateMap(iPlayer)
	war.updateMap(iPlayer)


def evacuate(iPlayer):
	if player(iPlayer).getPeriod() == -1:
		if iPlayer in dEvacuatePeriods:
			setPeriod(iPlayer, dEvacuatePeriods[iPlayer])
			
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
	if iPlayer == iThailand:
		setPeriod(iKhmer, iPeriodVietnam)
	
	if iPlayer == iGermany:
		setPeriod(iHolyRome, iPeriodAustria)


def onCollapse(iPlayer):
	if iPlayer == iChina:
		setPeriod(iMongolia, iPeriodYuan)


def onResurrection(iPlayer):
	if iPlayer == iGreece:
		setPeriod(iGreece, iPeriodModernGreece)
	
	if iPlayer == iChina:
		if year() > year(tBirth[iMongolia]):
			setPeriod(iChina, iPeriodMing)
	
	if iPlayer == iIndia:
		if year() < year(1900):
			setPeriod(iIndia, iPeriodMaratha)
		else:
			setPeriod(iIndia, -1)
	
	if iPlayer == iArabia:
		setPeriod(iArabia, iPeriodSaudi)
		
	# TODO: it was like this in onResurrection - figure out the intent
	if iPlayer in [iArabia, iMongolia]:
		setPeriod(iPlayer, -1)


def onCityAcquired(iPlayer, city, bConquest):
	iOwner = city.getOwner()

	if iPlayer == iOttomans:
		if city.at(68, 45):
			setPeriod(iOttomans, iPeriodOttomanConstantinople)
	
	if iTurks in [iPlayer, iOwner]:
		tTL, tBR = Areas.tCoreArea[iPersia]
		if isAreaControlled(iTurks, tTL, tBR):
			setPeriod(iTurks, iPeriodSeljuks)
		else:
			setPeriod(iTurks, -1)
			
	if iOwner == iByzantium:
		if bConquest and pByzantium.getNumCities() <= 4:
			setPeriod(iByzantium, iPeriodByzantineConstantinople)
	
	
def onCityBuilt(city):
	iOwner = city.getOwner()

	if iOwner == iPhoenicia:
		if city.at(58, 39) and getOwnedCoreCities(iPhoenicia) > 0:
			setPeriod(iPhoenicia, iPeriodCarthage)


def onVassalState(iMaster, iVassal, bCapitulated):
	if iVassal == iInca:
		setPeriod(iInca, iPeriodPeru)
		
	if iVassal == iChina:
		if bCapitulated and iMaster == iMongolia:
			setPeriod(iMongolia, iPeriodYuan)
			

def onPalaceMoved(city):
	iOwner = city.getOwner()
	
	if iOwner == iPhoenicia:
		if city.at(58, 39):
			setPeriod(iPhoenicia, iPeriodCarthage)


def onTechAcquired(iPlayer, iEra):
	if iPlayer == iSpain:
		if iEra == iRenaissance and pSpain.getPeriod() == -1:
			if pMoors.isAlive() and cities.owner(iMoors).region(rIberia).none():
				setPeriod(iSpain, iPeriodSpain)
				setPeriod(iMoors, iPeriodMorocco)
	
	if iPlayer == iJapan:
		if iEra == iIndustrial:
			setPeriod(iJapan, iPeriodMeiji)
	
	if iPlayer == iItaly:
		if iEra == iIndustrial:
			setPeriod(iItaly, iPeriodModernItaly)
	
	if iPlayer == iGermany:
		if iEra == iDigital:
			setPeriod(iGermany, iPeriodModernGermany)