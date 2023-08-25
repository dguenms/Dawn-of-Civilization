from Core import *
from Events import handler

from SettlerMaps import dPeriodSettlerMaps
from WarMaps import dPeriodWarMaps
from Areas import dPeriodCoreArea


@handler("playerPeriodChange")
def announcePeriodChange(iPlayer, iPeriod):
	if iPeriod in dPeriodSettlerMaps or iPeriod in dPeriodWarMaps or iPeriod in dPeriodCoreArea:
		message(iPlayer, "TXT_KEY_MESSAGE_PERIOD_AREA_CHANGE")