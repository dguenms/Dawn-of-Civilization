from Consts import *
from RFCUtils import utils
from Stability import doResurrection


TL = (99, 43)
BR = (104, 48)

doResurrection(slot(iCivChina), utils.getAreaCities(utils.getPlotList(TL, BR)))