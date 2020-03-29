from Core import *
from RFCUtils import *

import Areas as areas
import SettlerMaps as settler
import WarMaps as war


dEvacuatePeriods = {
	iCivPhoenicia : iPeriodCarthage,
	iCivKhmer : iPeriodVietnam,
}


def setPeriod(iCiv, iPeriod):
	if not player(iCiv).isAlive():
		return

	player(iCiv).setPeriod(iPeriod)
	
	iPlayer = slot(iCiv)
	areas.updateCore(iPlayer)
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
		setPeriod(iCivIndia, iPeriodMaratha)
		setPeriod(iCivKhmer, iPeriodVietnam)
		setPeriod(iCivMoors, iPeriodMorocco)
		setPeriod(iCivSpain, iPeriodSpain)
		setPeriod(iCivHolyRome, iPeriodAustria)
		setPeriod(iCivOttomans, iPeriodOttomanConstantinople)


def onBirth(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iCivThailand:
		setPeriod(iCivKhmer, iPeriodVietnam)
	
	if iCiv == iCivGermany:
		setPeriod(iCivHolyRome, iPeriodAustria)


def onCollapse(iPlayer):
	if civ(iPlayer) == iCivChina:
		setPeriod(iCivMongols, iPeriodYuan)


def onResurrection(iPlayer):
	iCiv = civ(iPlayer)

	if iCiv == iCivGreece:
		setPeriod(iCivGreece, iPeriodModernGreece)
	
	if iCiv == iCivChina:
		if year() > year(dBirth[iCivMongols]):
			setPeriod(iCivChina, iPeriodMing)
	
	if iCiv == iCivIndia:
		if year() < year(1900):
			setPeriod(iCivIndia, iPeriodMaratha)
		else:
			setPeriod(iCivIndia, -1)
	
	if iCiv == iCivArabia:
		setPeriod(iCivArabia, iPeriodSaudi)
		
	# TODO: it was like this in onResurrection - figure out the intent
	if iCiv in [iCivArabia, iCivMongols]:
		setPeriod(iCiv, -1)


def onCityAcquired(iPlayer, city, bConquest):
	iOwner = city.getOwner()
	iCiv = civ(iPlayer)
	iOwnerCiv = civ(iOwner)

	if iCiv == iCivOttomans:
		if city.at(68, 45):
			setPeriod(iCivOttomans, iPeriodOttomanConstantinople)
	
	if iCivTurks in [iCiv, iOwnerCiv]:
		tTL, tBR = Areas.dCoreArea[iCivPersia]
		if isAreaControlled(slot(iCivTurks), tTL, tBR):
			setPeriod(iCivTurks, iPeriodSeljuks)
		else:
			setPeriod(iCivTurks, -1)
			
	if iOwnerCiv == iCivByzantium:
		if bConquest and player(iCivByzantium).getNumCities() <= 4:
			setPeriod(iCivByzantium, iPeriodByzantineConstantinople)
	
	
def onCityBuilt(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)

	if iOwnerCiv == iCivPhoenicia:
		if city.at(58, 39) and getOwnedCoreCities(iOwner) > 0:
			setPeriod(iCivPhoenicia, iPeriodCarthage)


def onVassalState(iMaster, iVassal, bCapitulated):
	iMasterCiv = civ(iMaster)
	iVassalCiv = civ(iVassal)

	if iVassalCiv == iCivInca:
		setPeriod(iCivInca, iPeriodPeru)
		
	if iVassalCiv == iCivChina:
		if bCapitulated and iMasterCiv == iCivMongols:
			setPeriod(iCivMongols, iPeriodYuan)
			

def onPalaceMoved(city):
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)
	
	if iOwnerCiv == iCivPhoenicia:
		if city.at(58, 39):
			setPeriod(iCivPhoenicia, iPeriodCarthage)


def onTechAcquired(iPlayer, iEra):
	iCiv = civ(iPlayer)

	if iCiv == iCivSpain:
		if iEra == iRenaissance and player(iCiv).getPeriod() == -1:
			if player(iCivMoors).isAlive() and cities.owner(iCivMoors).region(rIberia).none():
				setPeriod(iCivSpain, iPeriodSpain)
				setPeriod(iCivMoors, iPeriodMorocco)
	
	if iCiv == iCivJapan:
		if iEra == iIndustrial:
			setPeriod(iCivJapan, iPeriodMeiji)
	
	if iCiv == iCivItaly:
		if iEra == iIndustrial:
			setPeriod(iCivItaly, iPeriodModernItaly)
	
	if iPlayer == iCivGermany:
		if iEra == iDigital:
			setPeriod(iCivGermany, iPeriodModernGermany)