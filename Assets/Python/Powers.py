from Core import *
from Events import handler


@handler("cityAcquired")
def colombianPower(iOwner, iPlayer, city, bConquest):
	if civ(iPlayer) == iColombia and bConquest:
		if city in cities.rectangle(tSouthCentralAmericaTL, tSouthCentralAmericaBR):
			city.setOccupationTimer(0)
