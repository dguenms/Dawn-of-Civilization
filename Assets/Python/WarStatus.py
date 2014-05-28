from CvPythonExtensions import *

gc = CyGlobalContext()

class WarStatus:

	### constructor ###
	
	def __init__(self, iOwnPlayer, iEnemyPlayer):
		self.iOwnPlayer = iOwnPlayer
		self.iEnemyPlayer = iEnemyPlayer
		
		self.iStartingTurn = gc.getGame().getGameTurn()
		
		self.iInitialPower = gc.getTeam(iOwnPlayer).getPower(False)
		self.iInitialCities = gc.getPlayer(iOwnPlayer).getNumCities()
		
		self.iDefeatedUnits = 0
		self.iConqueredCities = 0
		
	### getters and setters ###
	
	def getPlayerID(self):
		return self.iOwnPlayer
		
	def getEnemyID(self):
		return self.iEnemyPlayer
		
	def getStartingTurn(self):
		return self.iStartingTurn
		
	def getInitialPower(self):
		return self.iInitialPower
		
	def getInitialCities(self):
		return self.iInitialCities
		
	def getDefeatedUnits(self):
		return self.iDefeatedUnits
		
	def setDefeatedUnits(self, iNewValue):
		self.iDefeatedUnits = iNewValue
		
	def changeDefeatedUnits(self, iChange):
		self.iDefeatedUnits += iChange
		
	def getConqueredCities(self):
		return self.iConqueredCities
		
	def setConqueredCities(self, iNewValue):
		self.iConqueredCities = iNewValue
		
	def changeConqueredCities(self, iChange):
		self.iConqueredCities += iChange