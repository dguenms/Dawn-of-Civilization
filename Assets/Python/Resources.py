# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
#import Popup
import Consts as con
import RFCUtils # edead

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()

### Constants ###


# initialise bonuses variables

iHorse = con.iHorse
iBanana = con.iBanana
iCorn = con.iCorn
iCow = con.iCow
iPig = con.iPig
iSheep = con.iSheep
iWheat = con.iWheat
iSugar = con.iSugar
iWine = con.iWine
iCotton = con.iCotton
iDye = con.iDye
iRice = con.iRice
iClam = con.iClam
iFish = con.iFish
iCoffee = con.iCoffee
iTea = con.iTea
iTobacco = con.iTobacco
iSpices = con.iSpices
iIvory = con.iIvory
iIron = con.iIron

iCottage = con.iCottage
iSilk = con.iSilk
iRoad = 0
#Orka: Silk Road road locations
tSilkRoute = ((85,48), (86,49), (87,48), (88,47), (89,46), (90,47),(90,45),  (91,47),(91,45),  (92,48),(92,45),  (93,48),(93,46),  (94,47), (95,47), (96,47), (97,47), (98,47), (99,46))

class Resources:
       	
        def checkTurn(self, iGameTurn):


                #if (iGameTurn == 5): #otherwise it's picked by Portugal at the beginning
                #        gc.getMap().plot(49, 43).setImprovementType(con.iHut)
			
		# Tamils
		if iGameTurn == getTurnForYear(-300)-1 and utils.getPlayerEnabled(con.iTamils):
			gc.getMap().plot(90, 29).setBonusType(iFish)

                #Orka: Silk Road
                if (iGameTurn == getTurnForYear(-200)): 
                        for i in range( len(tSilkRoute) ):
                            gc.getMap().plot(tSilkRoute[i][0], tSilkRoute[i][1]).setRouteType(iRoad)
                
                #Orka: Silk Road
                if (iGameTurn == getTurnForYear(-100)):
                        CyGame().setPlotExtraYield(91, 45, YieldTypes.YIELD_FOOD, 2) #Khotan    
                        gc.getMap().plot(91, 45).setImprovementType(iCottage) #Khotan                               
                        CyGame().setPlotExtraYield(93, 48, YieldTypes.YIELD_FOOD, 2) #Turfan    
                        gc.getMap().plot(93, 48).setImprovementType(iCottage) #Turfan                            
                        #gc.getMap().plot(90, 45).setBonusType(iCotton) #Kashgar
                        #gc.getMap().plot(94, 47).setBonusType(iWheat) #Dunhuang
                        #gc.getMap().plot(96, 48).setBonusType(iSilk) #Dunhuang
                        CyGame().setPlotExtraYield(97, 47, YieldTypes.YIELD_FOOD, 2) #Wuwei    
                        gc.getMap().plot(97, 47).setImprovementType(iCottage) #Wuwei    
                        #CyGame().setPlotExtraYield(85, 38, YieldTypes.YIELD_FOOD, 2) #Lanzhou
                        #gc.getMap().plot(99, 46).setImprovementType(iCottage) #Lanzhou
			CyGame().setPlotExtraYield(95, 47, YieldTypes.YIELD_FOOD, 2) #Dunhuang
			CyGame().setPlotExtraYield(89, 46, YieldTypes.YIELD_FOOD, 2) #Kashgar

			gc.getMap().plot(88, 47).setPlotType(PlotTypes.PLOT_HILLS, True, True)
			gc.getMap().plot(88, 47).setRouteType(iRoad)
			gc.getMap().plot(88, 47).setBonusType(iSilk)
			gc.getMap().plot(85, 46).setBonusType(iSilk)

		#Leoreth: Hanseong's pig appears later so China isn't that eager to found Sanshan
		if iGameTurn == getTurnForYear(-50):
			gc.getMap().plot(108, 47).setBonusType(iPig)

		#Leoreth: change Indus tiles to desert floodplains in 0 AD
		if (iGameTurn == getTurnForYear(0)):
			for tPlot in [(86, 37), (86, 38), (87, 38)]:
				x, y = tPlot
				gc.getMap().plot(x,y).setBonusType(-1)
				gc.getMap().plot(x,y).setTerrainType(2, True, True)
				gc.getMap().plot(x,y).setFeatureType(3, 0)
			for tPlot in [(85, 38), (85, 37)]:
				x, y = tPlot
				gc.getMap().plot(x,y).setFeatureType(3, 0)

                if (iGameTurn == getTurnForYear(450)): #(dye added later to prevent Carthaginian UHV exploit)
                        gc.getMap().plot(53, 51).setBonusType(iDye) #France
                        gc.getMap().plot(53, 55).setBonusType(iDye) #England
                if utils.getScenario() >= con.i600AD: #late start condition
                        if (iGameTurn == getTurnForYear(600)): 
                                gc.getMap().plot(53, 51).setBonusType(iDye) #France
                                gc.getMap().plot(53, 55).setBonusType(iDye) #England

		# Leoreth: remove floodplains in Sudan and ivory in Morocco
		if iGameTurn == getTurnForYear(550):
			gc.getMap().plot(67, 30).setFeatureType(-1, 0)
			gc.getMap().plot(67, 31).setFeatureType(-1, 0)
			
			gc.getMap().plot(51, 36).setBonusType(-1)

		# Leoreth: replicate silk route in 600 AD
		if iGameTurn == getTurnForYear(600) and utils.getScenario() == con.i600AD:
                        CyGame().setPlotExtraYield(91, 45, YieldTypes.YIELD_FOOD, 2) #Khotan                               
                        CyGame().setPlotExtraYield(93, 48, YieldTypes.YIELD_FOOD, 2) #Turfan
                        CyGame().setPlotExtraYield(97, 47, YieldTypes.YIELD_FOOD, 2) #Wuwei
			CyGame().setPlotExtraYield(95, 47, YieldTypes.YIELD_FOOD, 2) #Dunhuang
			CyGame().setPlotExtraYield(89, 46, YieldTypes.YIELD_FOOD, 2) #Kashgar
			
		# Leoreth: prepare Tibet
		if iGameTurn == getTurnForYear(630)-1 and utils.getPlayerEnabled(con.iTibet):
			gc.getMap().plot(95, 43).setBonusType(iWheat)
			gc.getMap().plot(97, 44).setBonusType(iHorse)
		
		# Leoreth: for respawned Egypt
		if iGameTurn == getTurnForYear(900):
			gc.getMap().plot(71, 34).setBonusType(con.iIron)
			
                    
                if (iGameTurn == getTurnForYear(1100)):
                        #gc.getMap().plot(71, 30).setBonusType(iSugar) #Egypt
                        gc.getMap().plot(72, 24).setBonusType(iSugar) #East Africa
                        gc.getMap().plot(70, 17).setBonusType(iSugar) #Zimbabwe
                        gc.getMap().plot(67, 11).setBonusType(iSugar) #South Africa

                        gc.getMap().plot(66, 23).setBonusType(iBanana) #Central Africa
                        gc.getMap().plot(64, 20).setBonusType(iBanana) #Central Africa
			
			if utils.getPlayerEnabled(con.iCongo):
				gc.getMap().plot(61, 22).setBonusType(iCotton) #Congo
				gc.getMap().plot(63, 19).setBonusType(iIvory) #Congo
				gc.getMap().plot(61, 24).setBonusType(iIvory) #Cameroon

			gc.getMap().plot(57, 46).setBonusType(iWine) #Savoy
			gc.getMap().plot(57, 45).setBonusType(iClam) #Savoy
			
		# Leoreth: route to connect Karakorum to Beijing and help the Mongol attackers
		if iGameTurn == getTurnForYear(con.tBirth[con.iMongolia]):
			for tPlot in [(101, 48), (100, 49), (100, 50), (99, 50)]:
				x, y = tPlot
				gc.getMap().plot(x, y).setRouteType(iRoad)

                if (iGameTurn == getTurnForYear(1250)):
                        gc.getMap().plot(57, 52).setBonusType(iWheat) #Amsterdam
			gc.getMap().plot(96, 37).setBonusType(iFish)  #Calcutta/Dhaka/Pagan

		if iGameTurn == getTurnForYear(1350):
			gc.getMap().plot(102, 35).setFeatureType(-1, 0) #remove jungle in Vietnam

		if (iGameTurn == getTurnForYear(1500)):
			gc.getMap().plot(36, 54).setFeatureType(4, 2) #Forest in Newfoundland
			gc.getMap().plot(36, 54).setTerrainType(3, True, True) #Tundra in Newfoundland
			gc.getMap().plot(36, 54).setBonusType(-1) #remove marsh in Newfoundland
			
			gc.getMap().plot(56, 54).setBonusType(iFish) #Amsterdam
                        
                if (iGameTurn == getTurnForYear(1600)):
                        gc.getMap().plot(28, 46).setBonusType(iCow) #Washington area
                        gc.getMap().plot(30, 49).setBonusType(iCow) #New York area
                        gc.getMap().plot(25, 49).setBonusType(iCow) #Lakes
                        gc.getMap().plot(23, 42).setBonusType(iCow) #Jacksonville area
                        gc.getMap().plot(18, 46).setBonusType(iCow) #Colorado 
                       # gc.getMap().plot(11, 47).setBonusType(iCow) #California
                        gc.getMap().plot(20, 45).setBonusType(iCow) #Texas
                        gc.getMap().plot(37, 14).setBonusType(iCow) #Argentina
                        gc.getMap().plot(33, 11).setBonusType(iCow) #Argentina
                        gc.getMap().plot(35, 10).setBonusType(iCow) #Pampas

                        gc.getMap().plot(24, 43).setBonusType(iCotton) #near Florida
                        gc.getMap().plot(23, 45).setBonusType(iCotton) #Louisiana
                        gc.getMap().plot(22, 44).setBonusType(iCotton) #Louisiana
                        gc.getMap().plot(13, 45).setBonusType(iCotton) #California
                        
                        gc.getMap().plot(22, 49).setBonusType(iPig) #Lakes
                        
                        gc.getMap().plot(21, 50).setBonusType(iWheat) #Canadian border
                        gc.getMap().plot(19, 48).setBonusType(iWheat) #Midwest

                        gc.getMap().plot(22, 33).setBonusType(iBanana) #Guatemala
                        gc.getMap().plot(27, 31).setBonusType(iBanana) #Colombia
                        gc.getMap().plot(43, 23).setBonusType(iBanana) #Brazil
                        gc.getMap().plot(39, 26).setBonusType(iBanana) #Brazil

                        gc.getMap().plot(49, 44).setBonusType(iCorn) #Galicia
                        gc.getMap().plot(54, 48).setBonusType(iCorn) #France
                        gc.getMap().plot(67, 47).setBonusType(iCorn) #Romania

                        gc.getMap().plot(106, 50).setBonusType(iCorn) #Manchuria
			
			gc.getMap().plot(92, 35).setBonusType(iSpices) #Deccan
			
			# remove floodplains in Transoxania
			for tuple in [(82, 47), (83, 46), (85, 49)]:
				x, y = tuple
				gc.getMap().plot(x, y).setFeatureType(-1, 0)
                       

                if (iGameTurn == getTurnForYear(1700)):
                        gc.getMap().plot(26, 45).setBonusType(iHorse) #Washington area                        
                        gc.getMap().plot(21, 48).setBonusType(iHorse) #Midwest
                        gc.getMap().plot(19, 45).setBonusType(iHorse) #Texas
                        gc.getMap().plot(40, 25).setBonusType(iHorse) #Brazil
                        gc.getMap().plot(33, 10).setBonusType(iHorse) #Buenos Aires area
                        gc.getMap().plot(32, 8).setBonusType(iHorse) #Pampas

                        gc.getMap().plot(27, 36).setBonusType(iSugar) #Caribbean
                        gc.getMap().plot(39, 25).setBonusType(iSugar) #Brazil
                        gc.getMap().plot(37, 20).setBonusType(iSugar) #inner Brazil
			gc.getMap().plot(29, 37).setBonusType(iSugar) #Hispaniola

                        gc.getMap().plot(104, 52).setBonusType(iCorn) #Manchuria
                        gc.getMap().plot(89, 36).setBonusType(iCorn) #India
			
			gc.getMap().plot(38, 18).setBonusType(iCoffee) #Brazil
			gc.getMap().plot(39, 20).setBonusType(iCoffee) #Brazil
			gc.getMap().plot(38, 22).setBonusType(iCoffee) #Brazil
			gc.getMap().plot(27, 30).setBonusType(iCoffee) #Colombia
			gc.getMap().plot(29, 30).setBonusType(iCoffee) #Colombia
			gc.getMap().plot(26, 27).setBonusType(iCoffee) #Colombia
			gc.getMap().plot(104, 25).setBonusType(iCoffee) #Java
			
			gc.getMap().plot(67, 44).setBonusType(iTobacco) #Turkey
			
			gc.getMap().plot(90, 35).setBonusType(iTea) #West Bengal
			
			gc.getMap().plot(39, 16).setBonusType(iFish) #Brazil
			
			gc.getMap().plot(27, 29).setPlotType(PlotTypes.PLOT_HILLS, True, True) #Bogota
			
		if iGameTurn == getTurnForYear(1800):
			gc.getMap().plot(17, 41).setBonusType(iHorse) # Mexico
			gc.getMap().plot(16, 42).setBonusType(con.iIron) # Mexico
			
			gc.getMap().plot(31, 10).setBonusType(iWine) # Mendoza, Argentina
			gc.getMap().plot(31, 6).setBonusType(iSheep) # Pampas, Argentina
			gc.getMap().plot(32, 11).setBonusType(iIron) # Argentina
			
			gc.getMap().plot(36, 18).setBonusType(iCorn) # Sao Paulo
			gc.getMap().plot(42, 18).setBonusType(iFish) # Rio de Janeiro

                if (iGameTurn == getTurnForYear(1850)):
                        gc.getMap().plot(12, 45).setBonusType(iWine) #California
                        gc.getMap().plot(31, 10).setBonusType(iWine) #Andes
			gc.getMap().plot(113, 12).setBonusType(iWine) #Barossa Valley, Australia

                        gc.getMap().plot(114, 11).setBonusType(iSheep) #Australia
                        gc.getMap().plot(116, 13).setBonusType(iSheep) #Australia
                        gc.getMap().plot(121, 6).setBonusType(iSheep) #New Zealand

                        gc.getMap().plot(19, 41).setBonusType(iHorse) #Mexico

                        gc.getMap().plot(58, 47).setBonusType(iRice) #Vercelli
                        gc.getMap().plot(12, 49).setBonusType(iRice) #California

                        gc.getMap().plot(11, 45).setBonusType(iFish) #California
			gc.getMap().plot(10, 45).setBonusType(iFish) #California
			gc.getMap().plot(87, 35).setBonusType(iFish) #Bombay

			gc.getMap().plot(115, 52).setBonusType(iCow) #Hokkaido
			
			gc.getMap().plot(1, 38).setBonusType(iSugar) #Hawaii
			gc.getMap().plot(5, 36).setBonusType(iBanana) #Hawaii
			
			
			
			# flood plains in California
			for tPlot in [(11, 46), (11, 47), (11, 48)]:
				x, y = tPlot
				gc.getMap().plot(x,y).setFeatureType(3, 0)




                
                #setImprovementType(ImprovementType eNewValue)
                #setPlotType(PlotType eNewValue, BOOL bRecalculate, BOOL bRebuildGraphics)
                #setTerrainType(TerrainType eNewValue, BOOL bRecalculate, BOOL bRebuildGraphics)


                        


            




                        
