## Civilization 4 (c) 2005 Firaxis Games
##
## name     : AStarTool.py
## author   : 12monkeys
## date     : 10.03.2006
## version  : 1.1
##
## Notes
##   - Must be initialized externally by calling init()
##
## Modified for The BUG Mod by EmperorFool


from CvPythonExtensions import *

import BugCore
PleOpt = BugCore.game.PLE

gc = CyGlobalContext()
		
#####################################################################
# Class : AStar
#####################################################################
# class provides functions to create a path from plot A to plot B for 
# a given unit. 
# Main function to be used from outsiede are : 
# 	generatePath()	: creates a path and prepares the reults
# 	getPath()		: retrurns the path if one has been found
#	generateArea()	: creates an area a unit can move to
#	getArea()		: returns the area if one has been created
# see the methods for further definitions
#####################################################################				
class AStar:
	
	def __init__(self):
		self.pOpenList 				= AStarList()
		self.pCloseList 			= AStarList()
		self.pTargetPlot 			= None
		self.pFromPlot 				= None
		self.pUnit 					= None
		self.fHeuristicMvmtFactor 	= 0.0 				# possible smallest cost value a move from plot to plot will take
		self.fHeuristicTieBreak		= float(1.0/1000.0) 	# assuming the paths are shorter than 400 steps
		self.bResultValid			= false
		self.iLoopCount				= 0
		self.eDomain 				= 0
		self.bIgnoreMovesLeft		= false
		self.MODE_AREA				= 'A'
		self.MODE_PATH				= 'P'
			
	# moves a plot from open list to close list
	def moveToClose(self, pPlot):
		pParent = self.pOpenList.getParent(pPlot)
		iGCost = self.pOpenList.getGCosts(pPlot)
		fHCost = self.pOpenList.getHCosts(pPlot)
		self.pCloseList.set(pPlot, pParent, iGCost, fHCost)
		self.pOpenList.delete(pPlot)
		
	# returns the minimum x-distance, considering the x-axis over-/underflow
	def getRealXDist(self, x1, x2):
		d1 = abs(x1-x2)
		d2 = abs(min(x1, x2)+CyMap().getGridWidth()-max(x1, x2))
		return min(d1, d2)
		
	# returns the minimum y-distance, considering the y-axis over-/underflow
	def getRealYDist(self, y1, y2):
		d1 = abs(y1-y2)
		d2 = abs(min(y1, y2)+CyMap().getGridHeight()-max(y1, y2))
		return min(d1, d2)
	
	# calculates the heuristic 
	def calcHeuristic(self, pPlot):
		if self.nMode == self.MODE_PATH:
			# using "diagonal distance" method
			H = self.fHeuristicMvmtFactor * max(self.getRealXDist(pPlot.getX(), self.pTargetPlot.getX()), self.getRealYDist(pPlot.getY(), self.pTargetPlot.getY()))
			# methods to calculate the tie-break value usding the vector cross-product (dot-product)
			dx1 = pPlot.getX() - self.pTargetPlot.getX()
			dy1 = pPlot.getY() - self.pTargetPlot.getY()
			dx2 = self.pFromPlot.getX() - pPlot.getX()
			dy2 = self.pFromPlot.getY() - pPlot.getY()
			cross = float(abs(dx1*dy2 - dx2*dy1))
			H += float(cross*0.001)
		elif self.nMode == self.MODE_AREA:
			# no heuristic if we want to find an area. THis ensures that the complete area is examined
			H = 0.0
		return H

	# calculates a factor for the heuristic for the heuristic
	def calculateHeuristicFactors(self):
		pUnitTypeInfo = gc.getUnitInfo(self.pUnit.getUnitType())
		self.eDomain = pUnitTypeInfo.getDomainType()
		if (self.eDomain == DomainTypes.DOMAIN_SEA):
			# all sea plots have movements costs of 60/plot
			self.fHeuristicMvmtFactor 	= 60.0
		else:
			# min possible movement costs of 12/plot
			self.fHeuristicMvmtFactor 	= 12.0 
			
	# checks in case of sea plots, if there is a landbridge between the two plots
	def fnCheckLandBridge(self, pPlot, x, y):
		pTestPlot = CyMap().plot(pPlot.getX()+x, pPlot.getY()+y)
		if not (pPlot.isCity() or pTestPlot.isCity()):
			pTestPlot = CyMap().plot(pPlot.getX()+x, pPlot.getY())
			if (pTestPlot.isCoastalLand()):
				pTestPlot = CyMap().plot(pPlot.getX(), pPlot.getY()+y)
				if (pTestPlot.isCoastalLand()):
					return true
		return false
			
	# returns an adjacent plots reletaive to the coordinates of pPlot.
	# takes consideration of x and/or y overlows or underflows
	def getNewPlot(self, pPlot, dx, dy):
		x = pPlot.getX()+dx
		y = pPlot.getY()+dy
		# check x underflow
		if x < 0:
			x += CyMap().getGridWidth()
		# check x overflow
		elif x >= CyMap().getGridWidth():
			x -= CyMap().getGridWidth()
		# check y underflow
		if y < 0:
			y += CyMap().getGridHeight()
		# check y overflow
		elif y >= CyMap().getGridHeight():
			y -= CyMap().getGridHeight()
		return CyMap().plot(x, y)
		
	# core function of the A* algorithm
	# calculates the adjacents and puts them on the open list together wth the moving costs.
	# in case of area check, the heuristic is zero.
	def addAdjacents(self, pPlot):
		# loops for adjacent plots
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				# ignore center plot
				if not (dx == 0 and dy == 0):
					# create a plot objects
					pNewPlot = self.getNewPlot(pPlot, dx, dy)
					# check in case sof a sea unit, if there is a land bridge to cross
					if (dx != 0) and (dy != 0) and (self.eDomain == DomainTypes.DOMAIN_SEA):
						bCont = not self.fnCheckLandBridge(pPlot, dx, dy)
					else: 
						bCont = true
					if bCont:
						# check if the plot is passable
						if self.pUnit.canMoveOrAttackInto(pNewPlot, true):
							# check if the plot is already on the close list
							if not self.pCloseList.exists(pNewPlot):
								# calculate movement cost from root plot to new plot
								if self.pCloseList.exists(pPlot):
									iParentGCosts = self.pCloseList.getGCosts(pPlot)
								else:
									iParentGCosts = self.pOpenList.getGCosts(pPlot)
								iGCosts = pPlot.movementCost(self.pUnit, pNewPlot)+iParentGCosts
								if (self.bIgnoreMovesLeft) or (iGCosts <= self.iMovesLeft):
									# calculate heuristics cost new plot to targetplot
									fHCosts = self.calcHeuristic(pNewPlot)
									# calculate total costs new plot to targetplot
									fFCosts = float(iGCosts) + fHCosts
									# checks if the plot is on the open list already
									if self.pOpenList.exists(pNewPlot):
										# check if the already stored costs are less than the actual ones
										if iGCosts <= self.pOpenList.getGCosts(pNewPlot):
											self.pOpenList.set(pNewPlot, pPlot, iGCosts, fHCosts)
									else:
										# add it to the open list
										self.pOpenList.set(pNewPlot, pPlot, iGCosts, fHCosts)
						else:
							if self.nMode == self.MODE_AREA:
								self.pCloseList.set(pNewPlot, pPlot, -1, 0)
		return 
	
	# 
	# returns the path data which has been generate by "generatePath()" method.
	# It only returns a result when there is a valid result stored. If there is 
	# no valid result, the function returns an empty list
	# Attention : The first element of the returned list, is the last plot of the path!!!
	# The Method should only be called, if the "generatePath()" method has been called before.
	#
	# Parameters:
	# 	none
	# Returns: 
	# 	list in the format [(xn,yn), .... , (x2,y2), (x1,y1), (x0,y0)]
	# 	where 
	#		(xn,yn) : is the to-plot tuple and 
	#		(x0,y0) : is the from-plot tuple. x and y are ints.
	# 
	def getPath(self):
		lPath = []
		if self.bResultValid:
			pWorkPlot 	= self.pTargetPlot
			pParentPlot	= self.pTargetPlot
			while true:
				# adding target plot to the path
				lPath.append(self.pCloseList.getXY(pWorkPlot))
				# looking for the parent of the 
				pParentPlot = self.pCloseList.getParent(pWorkPlot)
				# make parent the work plot
				pWorkPlot = pParentPlot
				# check if we reached from plot
				if (pWorkPlot.getX() == self.pFromPlot.getX()) and (pWorkPlot.getY() == self.pFromPlot.getY()):
					break
		return lPath			
			
	#
	# tries to find a path from plot A to B and returns the overall movement costs for 
	# the unit. If no path could be found -1 is returned.
	# To get the path itself, the method getPath() must be called afterwards.
	# 
	# Parameters:
	# 	pUnit			: CyUnit 
	# 	pFromPlot 		: CyPlot
	# 	pToPlot 		: CyPlot
	# 	bIgnoreMovesLeft: bool
	# Returns:
	#	int 		(the costs to get from pFromPlot to pToPlot. -1 if no path could be found)
	#
	# The parameter "bIgnoreMovesLeft" can be used to reduce execution time. If the parameter is true, 
	# the algorithm stops a single path examiation if the remaining moves of a unit are not enough 
	# to reach the target plot. This significantly speeds up the algorithm in case you want to look for the 
	# the movable area. 
	# The parameter should be set to false in case you want to find a path from plot A to B without 
	# cost restrictions.
	# 
	def generatePath(self, pUnit, pFromPlot, pToPlot, bIgnoreMovesLeft):
	
		# clear the actual results
		self.bResultValid = false
		self.pOpenList.clear()
		self.pCloseList.clear()
		self.nMode = self.MODE_PATH
		
		# setting some variables
		self.pTargetPlot 		= pToPlot
		self.pFromPlot 			= pFromPlot
		self.pUnit 				= pUnit
		pNewPlot 				= pFromPlot
		pCurrentPlot			= pFromPlot
		bBreak 					= false
		self.iLoopCount			= 0
		self.iMovesLeft			= pUnit.movesLeft()
		self.bIgnoreMovesLeft	= bIgnoreMovesLeft

		# perfrom some checks ...
		if ((pFromPlot.getX() == pToPlot.getX()) and (pFromPlot.getY() == pToPlot.getY())):
			# From and To plot are equal -> break
			return -1
		if not (self.pUnit.canMoveOrAttackInto(pToPlot, true)):
			# To plot not passable -> break
			return -1		
		
		# calculates some values for the heuristic
		self.calculateHeuristicFactors()
		
		# put start plot on the open list
		self.pOpenList.set(pCurrentPlot, pCurrentPlot, 0, self.calcHeuristic(pNewPlot))	

		# repeat until target plot is reached
		while (true):
			self.addAdjacents(pCurrentPlot)
			self.moveToClose(pCurrentPlot)	
			if (self.pCloseList.exists(self.pTargetPlot)):
				# path found
				break
			if (self.pOpenList.len() == 0):
				# no path found
				bBreak = true
				break
			# find the plot with the lowest costs on the open list
			pCurrentPlot = self.pOpenList.findMinFCost()
			self.iLoopCount	+= 1

		# return the G-Costs of the Target Plot
		if bBreak:
			# no path found
			iReturn = -1
			self.bResultValid = false
		else:
			iReturn = int(self.pCloseList.getGCosts(pCurrentPlot))
			self.bResultValid = true
			
		return iReturn

	#
	# returns the area which has been found by "generateArea()". If no valid result is stored, an
	# empty list is retured.
	# The method should only be called, if the "generateArea()" method has been called before.
	# 
	# Parameters:
	# 	none
	# Returns:
	# 	list on the format [((x0,y0),c0), ((x1,y1),c1), ... , ((xn,yn),cn)]
	# 	where :
	#		(x,y) : is a tuple of ints describing the plots coordinates 
	#		c : the movements costs to get to the plot. -1 if the plot is impassable 
	# 
	def getArea(self):
		lArea = []
		if self.bResultValid:
			for i in range(self.pCloseList.len()):
				if i == 0:
					lAPlot = self.pCloseList.getFirst()
				else:
					lAPlot = self.pCloseList.getNext()
				iCosts = self.pCloseList.getGCosts(CyMap().plot(lAPlot[0], lAPlot[1]))
				lArea.append((lAPlot, iCosts))
		return lArea		

	#
	# creates an area a unit can move to within its remaining movement points. 
	# the function always returns 1, because even an empty list is a result.
	# to get the area itself, after the generateArea function, the method getArea() must be called
	#
	# Paramters : 
	#	pUnit		: CyUnit 
	#	pFromPlot 	: CyPlot
	# Returns : 
	#	int 		(constant 1)
	#
	def generateArea(self, pUnit, pFromPlot):
		
		# clear the actual results
		self.bResultValid = false
		self.pOpenList.clear()
		self.pCloseList.clear()
		self.nMode = self.MODE_AREA
		
		# setting some variables
		self.pTargetPlot 		= None
		self.pFromPlot 			= pFromPlot
		self.pUnit 				= pUnit
		pNewPlot 				= pFromPlot
		pCurrentPlot			= pFromPlot
		bBreak 					= false
		self.iLoopCount			= 0
		self.iMovesLeft			= pUnit.movesLeft()
		self.bIgnoreMovesLeft	= false

		
		# calculates some values for the heuristic
		self.calculateHeuristicFactors()
		
		# put start plot on the open list
		self.pOpenList.set(pCurrentPlot, pCurrentPlot, 0, self.calcHeuristic(pNewPlot))	

		# repeat until target plot is reached
		while (true):
			self.addAdjacents(pCurrentPlot)
			self.moveToClose(pCurrentPlot)	
			if (self.pOpenList.len() == 0):
				# list is empty -> all plots are examined
				break
			# find the plot with the lowest costs on the open list
			pCurrentPlot = self.pOpenList.findMinFCost()
			self.iLoopCount	+= 1

		# return the G-Costs of the Target Plot
		iReturn = 1
		self.bResultValid = true
		
		return iReturn
		
		
#####################################################################
# Class : AStarMoveArea
#####################################################################
# class provides functions to create a list of plots a unit can move 
# within its left moves. It also provides some functions to display
# and clear the this area.
# Main function to be used from outsiede are : 
# 	highlightMoveArea()		: calculates and highlights the area the can move to and computes the plot colors
#	dehighlightMoveArea()	: clears the display of that area
# see the methods for further definitions
# 
# the colors of the signle plots can be set in the __init__ section of the class
# COLOR_CLEAR can be used for no highlighting at all
#####################################################################		
class AStarMoveArea:

	def __init__(self):
		self.dPlotList 					= {}
		self.AS 						= AStar()
		self.pUnit 						= 0
		self.pFromPlot 					= 0
		self.PLE_HIGHLIGHT_PLOTS	 	= PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS 
		self.lArea 						= []
		self.iActivePlayerTeam			= 0
		self.iActivePlayer				= 0
		
		# color values
		self.COL_NO						= "COLOR_CLEAR"
		
	# converts a CyPlot into a tuple (x,y)
	def getPlotXY(self, pPlot):
		return (pPlot.getX(), pPlot.getY())
		
	# checks if there are any units on the plot and returns the corresponding color
	def checkUnit(self, pPlot):
		iNumUnits = pPlot.getNumUnits()
		bEnemy = false
		bNeutral = false
		bBarbarian = false
		for i in range(iNumUnits):
			pUnit = pPlot.getUnit(i)
			iTeam = pUnit.getTeam()
			if (iTeam == self.iActivePlayerTeam or pUnit.isCounterSpy()):
				continue
			iInvisibleType = pUnit.getInvisibleType()
			if (iInvisibleType != InvisibleTypes.NO_INVISIBLE):
				for j in range(self.pUnit.getNumSeeInvisibleTypes()):
					if (iInvisibleType == self.pUnit.getSeeInvisibleType(j)):
						break
				else:
					continue
			if (gc.getTeam(iTeam).isBarbarian()):
				bBarbarian = true
			elif (gc.getTeam(iTeam).isAtWar(self.iActivePlayerTeam)):
				bEnemy = true
			else:
				bNeutral = true
		if bEnemy:
			return PleOpt.MH_Color_Enemy_Unit()
		elif bBarbarian:
			return PleOpt.MH_Color_Barbarian_Unit()
		elif bNeutral:
			return PleOpt.MH_Color_Neutral_Unit()
		return PleOpt.MH_Color_Passable_Terrain()

	# checks if there forwign territory on the plot and returns the corresponding color
	def checkTerritory(self, pPlot):
		iPlayer = pPlot.getRevealedOwner(self.iActivePlayerTeam, false)
		pPlayer = gc.getPlayer(iPlayer)
		iTeam = pPlot.getRevealedTeam(self.iActivePlayerTeam, false)
		pTeam = gc.getTeam(iTeam)
		if pPlot.isRevealedGoody(iTeam):
			if (pPlot.getImprovementType() == 3):#ImprovementTypes.IMPROVEMENT_GOODY_HUT):
				return PleOpt.MH_Color_Passable_Barbarian_Territory()
		elif (iPlayer == PlayerTypes.NO_PLAYER) or (iPlayer == self.iActivePlayer):
			return PleOpt.MH_Color_Passable_Terrain()
		elif pTeam.isAtWar(self.iActivePlayerTeam):
			return PleOpt.MH_Color_Passable_Enemy_Territory()
		else:
			return PleOpt.MH_Color_Passable_Neutral_Territory()			
	
	# checks if there are revelaed plots adjacent to the given plot
	def checkAdjacentRevealed(self, pPlot):
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				if not (dx == 0 and dy == 0):
					if CyMap().plot(pPlot.getX()+dx, pPlot.getY()+dy).isRevealed(self.iActivePlayerTeam, false):
						return true
		return false
	
	# handles the color for a plot
	def setPlotColor(self, x, y, iCosts):
		pPlot = CyMap().plot(x, y)
		tPlot = (x, y)
		self.dPlotList[tPlot] = self.COL_NO
		# check impassable
		if iCosts == -1:
			if (pPlot.isWater() and (self.eDomain == DomainTypes.DOMAIN_SEA)) or ((not pPlot.isWater()) and (self.eDomain == DomainTypes.DOMAIN_LAND)):
				self.dPlotList[tPlot] = PleOpt.MH_Color_Impassable_Terrain()
		# check if plot is reachable
		elif iCosts <= self.iMovesLeft:
			# check if the plot is reavealed
			if pPlot.isRevealed(self.iActivePlayerTeam, false):
				# check if a unit at that plot
				if pPlot.isUnit() and pPlot.isVisible(self.iActivePlayerTeam, false):
					self.dPlotList[tPlot] = self.checkUnit(pPlot)
				# check if the plot is foreign territory
				elif pPlot.isVisible(self.iActivePlayerTeam, false):
					self.dPlotList[tPlot] = self.checkTerritory(pPlot)
				# nothing special with that plot
				else:
					self.dPlotList[tPlot] = PleOpt.MH_Color_Passable_Terrain()
			else:
				if self.checkAdjacentRevealed(pPlot):
					self.dPlotList[tPlot] = PleOpt.MH_Color_Passable_Terrain()
				else:
					self.dPlotList[tPlot] = self.COL_NO		
	
	#
	# highlights the area a unit can move to with its remaining movement points
	#
	# Parameters:
	# 	pUnit : CyUnit
	# Returns:
	# 	int		(constant 1)
	# 
	def highlightMoveArea(self, pUnit):
		# init some variables
		self.pUnit 				= pUnit
		self.pFromPlot 			= pUnit.plot()
		self.dPlotList 			= {}
		self.iMovesLeft 		= self.pUnit.movesLeft()
		pUnitTypeInfo 			= gc.getUnitInfo(self.pUnit.getUnitType())
		self.eDomain 			= pUnitTypeInfo.getDomainType()
		self.iActivePlayer 		= CyGame().getActivePlayer()
		pActivePlayer 			= gc.getPlayer(self.iActivePlayer)
		self.iActivePlayerTeam 	= pActivePlayer.getTeam()
		
		# add from plot to OK list
		self.dPlotList[self.getPlotXY(self.pFromPlot)] = 0

		# creates the infromation of the moveable area
		self.AS.generateArea(self.pUnit, self.pFromPlot)
		self.lArea = self.AS.getArea()
		
		# analyze data and set plot colors
		for i in range(len(self.lArea)):
			tItem = self.lArea[i]
			self.setPlotColor(tItem[0][0], tItem[0][1], tItem[1])
				
		# highlight the area
		self.highlightMoves()
		return 1
	
	# displays the area on the screen
	def highlightMoves(self):
		for plot, color in self.dPlotList.items(): 
			if color != self.COL_NO:
				CyEngine().addColoredPlotAlt(plot[0], plot[1], PlotStyles.PLOT_STYLE_TARGET, self.PLE_HIGHLIGHT_PLOTS, color, .5)

	#
	# clears the disaply of the area 
	#
	# Parameters:
	# 	none
	# Returns:
	# 	int		(constant 1)
	# 
	def dehighlightMoveArea(self):
		CyEngine().clearColoredPlots(self.PLE_HIGHLIGHT_PLOTS)
		return 1
	

	
#####################################################################
# Class : AStarPlot
#####################################################################
# class which is used to handle a specific plot format
# the plot data is stored as tuple in the format (x, y)
# class provides several function to handle this format 
# Only for internal use. 
#####################################################################		
class AStarPlot:
	
	def __init__(self):
		self.lPlot = (-1, -1)
		self.IDX_X = 0
		self.IDX_Y = 1
		
	# clears plot data
	def clear(self):
		self.lPlot = (-1, -1)
		
	# x, y : ints
	def setXY(self, x, y):
		self.lPlot = (x, y)
		
	# pPlot: CyPlot
	def setXYplot(self, pPlot):
		self.lPlot = (pPlot.getX(), pPlot.getY())
		
	# return x: int
	def getX(self):
		return self.lPlot[self.IDX_X]

	# return y: int
	def getY(self):
		return self.lPlot[self.IDX_Y]

	# x, y : ints
	# return (x,y)
	def getXY(self):
		return (self.getX(), self.getY())
		
	# pCompPlot: AStarPlot()
	# returns true if plot coords are equal
	def compare(self, pCompPlot):
		if (self.getX() == pCompPlot.getX()) and (self.getY() == pCompPlot.getY()):
			return true
		else:
			return false

			
#####################################################################
# Class : AStarList
#####################################################################
# class wto handle the open and close list for the AStar algorithm
# for internal use only
#####################################################################		
class AStarList:
	
	def __init__(self):
		self.dList = {}
		self.IDX_PARENT = 0
		self.IDX_GCOSTS = 1
		self.IDX_HCOSTS = 2
		self.IDX_FCOSTS = 3
		self.IDX_X = 0
		self.IDX_Y = 1
		self.maxCost = 9999999.9

	# clears the list
	def clear(self):
		self.dList = {}

	# creates a AStarPlot 
	# x, y: int
	# return: AStarPlot
	def makeAPlotXY(self, x, y):
		pAPlot = AStarPlot()
		pAPlot.setXY(x, y)
		return pAPlot
		
	# creates a AStarPlot 
	# pPlot = CyPlot
	# return: AStarPlot
	def makeAPlot(self, pPlot):
		return self.makeAPlotXY(pPlot.getX(), pPlot.getY())
		
	# sets all plot data
	# pAParent: AStarPlot, others are floats
	# return: ((x,y), int, float, float)
	def setPlotData(self, pAParent, iGCosts, fHCosts, fFCosts):
		return (pAParent, iGCosts, fHCosts, fFCosts)

	# returns all plot data
	# pAPlot: AStarPlot
	# return: ((x,y), float, float, float)
	def getPlotData(self, pAPlot):
		return self.dList[pAPlot.getXY()]

		
	# adds the complete plot to the list
	# pThisPlot, pParentPlot : CyPlot
	# iGCosts, fHCosts : int, float
	# if plot already exists, it will be overwritten
	def set(self, pThisPlot, pParentPlot, iGCosts, fHCosts):
		pAThisPlot = self.makeAPlot(pThisPlot)
		pAParentPlot = self.makeAPlot(pParentPlot)
		self.dList[pAThisPlot.getXY()] = self.setPlotData(pAParentPlot, iGCosts, fHCosts, float(iGCosts)+float(fHCosts))
			
	# pPlot : CyPlot
	# deletes the plot from the list
	def delete(self, pPlot):
		pAPlot = self.makeAPlot(pPlot)
		if self.dList.has_key(pAPlot.getXY()):
			del self.dList[pAPlot.getXY()]
			return true
		else:
			return false
			
	# pPlot : CyPlot
	# returns the g-costs as float
	def getGCosts(self, pPlot):
		pAPlot = self.makeAPlot(pPlot)
		return float(self.dList[pAPlot.getXY()][self.IDX_GCOSTS])

	# pPlot : CyPlot
	# returns the h-costs as float
	def getHCosts(self, pPlot):
		pAPlot = self.makeAPlot(pPlot)
		return float(self.dList[pAPlot.getXY()][self.IDX_HCOSTS])

	# pPlot : CyPlot
	# returns the f-costs as float
	def getFCosts(self, pPlot):
		pAPlot = self.makeAPlot(pPlot)
		return float(self.dList[pAPlot.getXY()][self.IDX_FCOSTS])

	# pPlot : CyPlot
	# returns the parent plot of the passed plot as CyPlot
	def getParent(self, pPlot):
		pAPlot = self.makeAPlot(pPlot)
		pAPlotData = self.getPlotData(pAPlot)
		x = pAPlotData[self.IDX_PARENT].getX()
		y = pAPlotData[self.IDX_PARENT].getY()
		return CyMap().plot(x, y)
		
	# returns the coords of a plot	(x,y)
	# pPlot: CyPlot
	def getXY(self, pPlot):
		pAPlot = self.makeAPlot(pPlot)
		return pAPlot.getXY()
		
	# pPlot : CyPlot
	# returns true if the plot exists in the list
	def exists(self, pPlot):
		pAPlot = self.makeAPlot(pPlot)
		if self.dList.has_key(pAPlot.getXY()):
			return true
		return false

	# pPlot : CyPlot
	# returns AStarPlot if found, else ()
	def search(self, pPlot):
		pAPlot = self.makeTPlot(pPlot)
		if self.dList.has_key(pAPlot.getXY()):
			return self.dList[(pAPlot.getXY())]
		return ()

	# returns the number of items in the list
	def len(self):
		return len(self.dList)

	# looks for the element with the smallest f-costs and returns it as CyPlot
	def findMinFCost(self):
		fComp = self.maxCost
		for key, val in self.dList.items():
			lData = self.dList[key]
			if lData[self.IDX_FCOSTS] < fComp:
				fComp = lData[self.IDX_FCOSTS]
				retKey = key
		x = retKey[0]
		y = retKey[1]
		return CyMap().plot(x, y)
	
	# returns the first element in the dict as CyPlot and prepares to fetch the next
	def getFirst(self):
		self.lList = []
		self.iList = 0
		for key, val in self.dList.items():
			self.lList.append(key)
		return self.lList[0]
		
	# returns the next element in the dict as CyPlot. "getFirst" needs to be called before.
	def getNext(self):
		if self.iList < self.len():
			self.iList += 1
			return self.lList[self.iList]
		else:
			return ()
