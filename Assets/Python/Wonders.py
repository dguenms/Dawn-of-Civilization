from Core import *
from Events import handler


@handler("cityAcquired")
def escorial(iOwner, iPlayer, city):
	if player(iPlayer).isHasBuildingEffect(iEscorial):
		if city.isColony():
			capital = player(iPlayer).getCapitalCity()
			iGold = scale(10 + distance(capital, city))
			message(iPlayer, 'TXT_KEY_BUILDING_ESCORIAL_EFFECT', iGold, city.getName())	
			player(iPlayer).changeGold(iGold)