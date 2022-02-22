from RFCUtils import *
from Core import *
from Locations import *
from DynamicCivs import *

from Events import handler

from Scenario3000BC import scenario3000BC
from Scenario600AD import scenario600AD
from Scenario1700AD import scenario1700AD


SCENARIOS = {
	i3000BC: scenario3000BC,
	i600AD: scenario600AD,
	i1700AD: scenario1700AD,
}


def getScenario(iScenario=None):
	if iScenario is None:
		iScenario = scenario()
	
	return SCENARIOS[iScenario]