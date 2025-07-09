from Events import handler
from Core import *

InebuHedjCoord = (79, 43)

@handler("GameStart")
def BeginPyramids():
    pEgypt = player(iEgypt)
    cInebuHedj = city(InebuHedjCoord)

    # Begin production of Pyramids in Inebu-Hedj and force research of Masonry
    cInebuHedj.pushOrder(OrderTypes.ORDER_CONSTRUCT, iPyramids, -1, False, False, False, True)
    pEgypt.pushResearch(iMasonry, True)

    