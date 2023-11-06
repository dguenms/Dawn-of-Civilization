from Core import *
from Files import *
from Events import handler

from Areas import dPeriodCoreArea
from Periods import dPeriodNames


@handler("playerPeriodChange")
def announcePeriodChange(iPlayer, iPeriod):
	if iPeriod != -1:
		if FileMap("Settler/Period/%s.csv" % dPeriodNames[iPeriod]) or FileMap("War/Period/%s.csv" % dPeriodNames[iPeriod]) or iPeriod in dPeriodCoreArea:
			message(iPlayer, "TXT_KEY_MESSAGE_PERIOD_AREA_CHANGE")