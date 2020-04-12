# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
#import Popup
from Consts import *
from RFCUtils import * # edead
from StoredData import data


### Constants ###

# initialise bonuses variables

lSilkRoute = [(85,48), (86,49), (87,48), (88,47), (89,46), (90,47), (90,45), (91,47), (91,45), (92,48), (93,48), (93,46), (94,47), (95,47), (96,47), (97,47), (98,47), (99,46)]
lNewfoundlandCapes = [(34, 52), (34, 53), (34, 54), (35, 52), (36, 52), (35, 55), (35, 56), (35, 57), (36, 51), (36, 58), (36, 59)]

class Resources:

	# Leoreth: bonus removal alerts by edead
	def createResource(self, iX, iY, iBonus, createTextKey="TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", removeTextKey="TXT_KEY_MISC_EVENT_RESOURCE_EXHAUSTED"):
		"""Creates a bonus resource and alerts the plot owner"""
		plot = plot_(iX, iY)
		
		iRemovedBonus = plot.getBonusType(-1) # for alert
		
		if iRemovedBonus == iBonus:
			return
		
		plot.setBonusType(iBonus)
				
		if iBonus == -1:
			iImprovement = plot.getImprovementType()
			if iImprovement >= 0:
				if infos.improvement(iImprovement).isImprovementBonusTrade(iRemovedBonus):
					plot.setImprovementType(-1)
			
		iOwner = plot.getOwner()
		if iOwner >= 0: # only show alert to the tile owner
			bWater = plot.isWater()
			city = closestCity(plot, iOwner, same_continent=not bWater, coastal_only=bWater)
			
			if iRemovedBonus >= 0:
				self.notifyResource(iOwner, city, iX, iY, iRemovedBonus, removeTextKey)
			
			if iBonus >= 0:
				self.notifyResource(iOwner, city, iX, iY, iBonus, createTextKey)
					
	def notifyResource(self, iPlayer, city, iX, iY, iBonus, textKey):
		if not city: return
		
		if infos.bonus(iBonus).getTechReveal() == -1 or team(iPlayer).isHasTech(infos.bonus(iBonus).getTechReveal()):
			message(iPlayer, textKey, infos.bonus(iBonus).getText(), city.getName(), event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, button=infos.bonus(iBonus).getButton(), location=(iX, iY))

	def removeResource(self, iX, iY):
		"""Removes a bonus resource and alerts the plot owner"""
		if plot(iX, iY).getBonusType(-1) == -1: return
		self.createResource(iX, iY, -1)
       	
	def checkTurn(self, iGameTurn):
		
		# Gujarati horses appear later so Harappa cannot benefit too early
		if iGameTurn == year(-1000):
			self.createResource(88, 37, iHorse)
			
		# Assyrian copper appears later to prevent Babylonia from building too strong a defensive military
		if iGameTurn == year(-800):
			self.createResource(78, 42, iCopper)
			
		# Tamils, 300 BC
		elif iGameTurn == year(dBirth[iTamils])-1 and data.isCivEnabled(iTamils):
			self.createResource(90, 28, iFish)

		#Orka: Silk Road
		elif iGameTurn == year(-200): 
			for x, y in lSilkRoute:
				plot(x, y).setRouteType(iRouteRoad)
		
		#Orka: Silk Road
		elif iGameTurn == year(-100):
			plot(88, 47).setPlotType(PlotTypes.PLOT_HILLS, True, True)
			plot(88, 47).setRouteType(iRouteRoad)
			
			self.createResource(88, 47, iSilk)
			self.createResource(85, 46, iSilk)

		#Leoreth: Hanseong's pig appears later so China isn't that eager to found Sanshan
		elif iGameTurn == year(-50):
			self.createResource(108, 47, iPig)

		# Leoreth: remove floodplains in Sudan and ivory in Morocco and Tunisia
		elif iGameTurn == year(550):
			plot(67, 30).setFeatureType(-1, 0)
			plot(67, 31).setFeatureType(-1, 0)
			
			self.removeResource(51, 36)
			self.removeResource(58, 37)
			
		# Leoreth: prepare Tibet, 630 AD
		elif iGameTurn == year(dBirth[iTibet])-1 and data.isCivEnabled(iTibet):
			self.createResource(95, 43, iWheat)
			self.createResource(97, 44, iHorse)
			
		# Leoreth: obstacles for colonization
		elif iGameTurn == year(700):
			plot(35, 54).setFeatureType(iMud, 0)
			for x, y in lNewfoundlandCapes:
				plot(x, y).setFeatureType(iCape, 0)
				
			if player(iVikings).isHuman():
				plot(41, 58).setFeatureType(-1, 0)
		
		# Leoreth: for respawned Egypt
		elif iGameTurn == year(900):
			self.createResource(71, 34, iIron)
		
		# Leoreth: New Guinea can be settled
		elif iGameTurn == year(1000):
			plot(113, 25).setFeatureType(-1, 0)
		    
		elif iGameTurn == year(1100):
			#plot(71, 30).setBonusType(iSugar) #Egypt
			
			self.createResource(72, 24, iSugar) # East Africa
			self.createResource(70, 17, iSugar) # Zimbabwe
			self.createResource(67, 11, iSugar) # South Africa
			
			self.createResource(66, 23, iBanana) # Central Africa
			self.createResource(64, 20, iBanana) # Central Africa
			
			if data.isCivEnabled(iCongo):
				self.createResource(61, 22, iCotton) # Congo
				self.createResource(63, 19, iIvory) # Congo
				self.createResource(61, 24, iIvory) # Cameroon
			
			self.createResource(57, 46, iWine) # Savoy
			self.createResource(57, 45, iClam) # Savoy
			
			self.createResource(50, 44, iIron) # Portugal
			
			self.removeResource(87, 49) # Orduqent
			self.removeResource(89, 51) # Orduqent
			
		# Leoreth: route to connect Karakorum to Beijing and help the Mongol attackers
		elif iGameTurn == year(dBirth[iMongols]):
			for x, y in [(101, 48), (100, 49), (100, 50), (99, 50)]:
				plot(x, y).setRouteType(iRouteRoad)
				
			# silk near Astrakhan
			self.createResource(78, 51, iSilk)

		if iGameTurn == year(1250):
			#plot(57, 52).setBonusType(iWheat) #Amsterdam
			self.createResource(96, 36, iFish) # Calcutta, Dhaka, Pagan

		elif iGameTurn == year(1350):
			plot(102, 35).setFeatureType(-1, 0) #remove rainforest in Vietnam

		elif iGameTurn == year(1500):
			plot(35, 54).setFeatureType(-1, 0) # remove Marsh in case it had been placed
			for x, y in lNewfoundlandCapes:
				plot(x, y).setFeatureType(-1, 0)
				
			# also remove Marsh on Port Moresby
			plot(116, 24).setFeatureType(-1, 0)
			
			self.createResource(56, 54, iFish) # Amsterdam
			self.createResource(57, 52, iWheat) # Amsterdam
			self.createResource(58, 52, iCow) # Amsterdam
			
		elif (iGameTurn == year(1600)):
			self.createResource(29, 52, iCow) # Montreal
			self.createResource(18, 53, iCow) # Alberta
			self.createResource(12, 52, iCow) # British Columbia
			self.createResource(28, 46, iCow) # Washington area
			self.createResource(30, 49, iCow) # New York area
			#self.createResource(25, 49, iCow) # Lakes
			self.createResource(23, 42, iCow) # Jacksonville area
			self.createResource(18, 46, iCow) # Colorado
			self.createResource(20, 45, iCow) # Texas
			self.createResource(37, 14, iCow) # Argentina
			self.createResource(33, 11, iCow) # Argentina
			self.createResource(35, 10, iCow) # Pampas
			
			self.createResource(24, 43, iCotton) # near Florida
			self.createResource(23, 45, iCotton) # Louisiana
			self.createResource(22, 44, iCotton) # Louisiana
			self.createResource(13, 45, iCotton) # California
			
			self.createResource(26, 49, iPig) # Lakes
			
			self.createResource(19, 51, iSheep) # Canadian border
			
			#self.createResource(21, 50, iWheat) # Canadian border
			self.createResource(19, 48, iWheat) # Midwest
			self.createResource(20, 53, iWheat) # Manitoba
			
			self.createResource(22, 33, iBanana) # Guatemala
			self.createResource(27, 31, iBanana) # Colombia
			self.createResource(43, 23, iBanana) # Brazil
			self.createResource(39, 26, iBanana) # Brazil
			
			self.createResource(49, 44, iCorn) # Galicia
			self.createResource(54, 48, iCorn) # France
			self.createResource(67, 47, iCorn) # Romania
			self.createResource(106, 50, iCorn) # Manchuria
			self.createResource(77, 52, iCorn) # Caricyn
			
			self.createResource(92, 35, iSpices) # Deccan
			plot(92, 35).setFeatureType(iRainforest, 0)
			
			# remove floodplains in Transoxania
			for x, y in [(82, 47), (83, 46), (85, 49)]:
				plot(x, y).setFeatureType(-1, 0)
		       

		elif iGameTurn == year(1700):
			self.createResource(16, 54, iHorse) # Alberta
			self.createResource(26, 45, iHorse) # Washington area
			self.createResource(21, 48, iHorse) # Midwest
			self.createResource(19, 45, iHorse) # Texas
			self.createResource(40, 25, iHorse) # Brazil
			self.createResource(33, 10, iHorse) # Buenos Aires area
			self.createResource(32, 8, iHorse) # Pampas
			self.createResource(30, 30, iHorse) # Venezuela
			
			self.createResource(27, 36, iSugar) # Caribbean
			self.createResource(39, 25, iSugar) # Brazil
			self.createResource(37, 20, iSugar) # inner Brazil
			self.createResource(29, 37, iSugar) # Hispaniola
			
			self.createResource(104, 52, iCorn) # Manchuria
			self.createResource(89, 36, iCorn) # India
			
			self.createResource(38, 18, iCoffee) # Brazil
			self.createResource(39, 20, iCoffee) # Brazil
			self.createResource(38, 22, iCoffee) # Brazil
			self.createResource(27, 30, iCoffee) # Colombia
			self.createResource(29, 30, iCoffee) # Colombia
			self.createResource(26, 27, iCoffee) # Colombia
			self.createResource(104, 25, iCoffee) # Java
			
			self.createResource(67, 44, iTobacco) # Turkey
			
			self.createResource(39, 16, iFish) # Brazil
			
			self.createResource(70, 59, iDeer) # St Petersburg
			
		elif iGameTurn == year(1800):
			if infos.constant('PLAYER_REBIRTH_MEXICO') != 0:
				self.createResource(17, 41, iHorse) # Mexico
				self.createResource(16, 42, iIron) # Mexico
				
			if infos.constant('PLAYER_REBIRTH_COLOMBIA') != 0:
				self.createResource(28, 31, iIron) # Colombia
			
			if data.isCivEnabled(iArgentina):
				self.createResource(31, 10, iWine) # Mendoza, Argentina
				self.createResource(31, 6, iSheep) # Pampas, Argentina
				self.createResource(32, 11, iIron) # Argentina
			
			if data.isCivEnabled(iBrazil):
				self.createResource(36, 18, iCorn) # Sao Paulo
				self.createResource(42, 18, iFish) # Rio de Janeiro

		elif iGameTurn == year(1850):
			self.createResource(12, 45, iWine) # California
			self.createResource(31, 10, iWine) # Andes
			self.createResource(113, 11, iWine) # Barossa Valley, Australia
			
			self.createResource(114, 11, iSheep) # Australia
			self.createResource(116, 13, iSheep) # Australia
			self.createResource(121, 6, iSheep) # New Zealand
			
			self.createResource(58, 47, iRice) # Vercelli
			self.createResource(12, 49, iRice) # California
			
			self.createResource(11, 45, iFish) # California
			#self.createResource(10, 45, iFish) # California
			self.createResource(87, 35, iFish) # Bombay
			
			self.createResource(115, 52, iCow) # Hokkaido
			
			self.createResource(1, 38, iSugar) # Hawaii
			self.createResource(5, 36, iBanana) # Hawaii
			
			self.createResource(108, 18, iCamel) # Australia
			
			# flood plains in California
			for x, y in [(11, 46), (11, 47), (11, 48)]:
				plot(x, y).setFeatureType(iFloodPlains, 0)