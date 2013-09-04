## Sid Meier's Civilization 4
## 
## This file is part of the UnitUpgradesPediaMod by Vovan
## Automatic layout algorithm by Progor
##

import string

from CvPythonExtensions import *

import CvUtil

# BUG - Mac Support - start
import BugUtil
BugUtil.fixSets(globals())
# BUG - Mac Support - end

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()

#The exception list allow you to completely hide a unit from the upgrade graph.
#This is useful for mods that use an unreachable unit to keep others from expiring.
#unitExceptionList = [UNIT_UNREACHABLE]
unitExceptionList = []

#The split lists let you split a particular unit into several different graphs, so it doesn't hold several
#upgrade paths together that would look better separate.  For instance, you might have a Ranger unit that
#upgrades from both a Scout and Warrior unit, but otherwise Scouting and Fighting units are in their own
#trees.  In this case, you would place the Ranger in the SplitIncoming list, to get the program to split up
#the incoming upgrades to Ranger so that Ranger shows up in both trees without holding them together.
#unitSplitIncoming = [UNIT_RANGER, UNIT_STYGIAN_GUARD]
unitSplitIncoming = []

#SplitOutgoing is similar, but for a unit that holds together two trees by what it upgrades to.  For instance,
#you might have a commoner unit that upgrades to Scout, Warrior, and Worker, while otherwise those units have
#their own trees.  Using the SplitOutgoing list will just put a commoner at the start of each of the 3 trees
#unitSplitOutgoing = [UNIT_DWARVEN_SOLDIER]
unitSplitOutgoing = []

#Default is 64, but if your graph is too large to fit in the Pedia window, specify a smaller button size here.
unitButtonSize = 64

#Margin refers to space from the edge and space between graphs
unitHorizontalMargin = 20
unitVerticalMargin = 20

#Spacing refers to the space between unit icons
unitHorizontalSpacing = 40
unitVerticalSpacing = 5

#The same concepts apply to the promotions graphs as to the unit graphs
promotionsExceptionList = []
promotionsSplitIncoming = []
promotionsSplitOutgoing = []
promotionsButtonSize = 64
promotionsHorizontalMargin = 20
promotionsVerticalMargin = 20
#promotionsHorizontalSpacing = 50
#promotionsVerticalSpacing = 5
promotionsHorizontalSpacing = 75
promotionsVerticalSpacing = 5


################################### BEGIN CLASS DEFINITIONS ###########################################
#Don't change below unless you know what you're doing

class Node:
	"This node holds all necessary information for a single unit"
	
	def __init__(self):
		self.x = 999
		self.y = 999
		self.upgradesTo = set()
		self.upgradesFrom = set()
		self.seen = False
		
	def __repr__(self):
		return "Node<x: %i, y: %i, to: %s, from: %s, seen: %s>"%(self.x, self.y, self.upgradesTo, self.upgradesFrom, self.seen)

class MGraph:
	"This Graph is a collection of unit Node's with multiple access methods for fast topological sorting"
	
	def __init__(self):
		self.graph = {}
		self.matrix = []
		self.depth = 0
		self.width = 0
	
	def __repr__(self):
		return "MGraph<depth: %i, width: %i, graph: %s, matrix: %s>"%(self.depth, self.width, self.graph, self.matrix)

## NOTE: PromotionsGraph subclass located at bottom of file.
class UnitUpgradesGraph:
	"The graph of unit upgrades"

	# Rearranged so that methods that need to be overridden by promotions graph are placed first.
	
	def __init__(self, pediaScreen):
		self.mGraphs = []
		self.horizontalMargin = unitHorizontalMargin
		self.verticalMargin = unitVerticalMargin
		self.horizontalSpacing = unitHorizontalSpacing
		self.verticalSpacing = unitVerticalSpacing
		self.pediaScreen = pediaScreen
		self.upgradesList = pediaScreen.UPGRADES_GRAPH_ID
		self.buttonSize = unitButtonSize
		self.exceptionList = unitExceptionList
		self.splitIncoming = unitSplitIncoming
		self.splitOutgoing = unitSplitOutgoing

	def getNumberOfUnits(self):
		return gc.getNumUnitClassInfos()
		
	def getUnitNumber(self, k):
		"Gets the id for the kth unit for the current active player"
		if (self.getActivePlayer() == -1):
			result = gc.getUnitClassInfo(k).getDefaultUnitIndex()
		else:
			result = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(k)
		return result
	
	def getUnitType(self, e):
		"Returns the type of the units with the specified id"
		return gc.getUnitInfo(e).getType()

	def getGraphEdges(self, graph):
		for unitA in graph.iterkeys():
			for numB in range(gc.getNumUnitClassInfos()):
				unitB = self.getUnitNumber(numB)
				if gc.getUnitInfo(unitA).getUpgradeUnitClass(numB):
					self.addUpgradePath(graph, unitA, unitB)

	def placeOnScreen(self, screen, unit, xPos, yPos):
		screen.setImageButtonAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, gc.getUnitInfo(unit).getButton(), xPos, yPos, self.buttonSize, self.buttonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, unit, 1)
			
	def unitToString(self, unit):
		return gc.getUnitInfo(unit).getDescription() + ":%d"%(unit, )
	
	################## Stuff to generate Unit Upgrade Graph ##################

	def addUpgradePath(self, graph, unitFrom, unitTo):

		# Check if unit numbers are valid
		if (unitFrom >= 0 and graph.has_key(unitFrom) and unitTo >= 0 and graph.has_key(unitTo)):
			graph[unitFrom].upgradesTo.add(unitTo)
			graph[unitTo].upgradesFrom.add(unitFrom)
			CvUtil.pyPrint(self.unitToString(unitFrom) + " upgrades to " + self.unitToString(unitTo) + ".")			

	def getActivePlayer(self):
		"Gets the id of the active player for UU upgrades"
		return gc.getGame().getActivePlayer()

	def getMedianY(self, mGraph, unitSet):
		"Returns the average Y position of the units in unitSet"
		
		if (len(unitSet) == 0):
			return -1
		sum = 0.0
		num = 0.0
		for unit in unitSet:
			sum += mGraph.graph[unit].y
			num += 1
		return sum/num
	
	def swap(self, mGraph, x, yA, yB):
		"Swaps two elements in a given row"
	
		unitA = mGraph.matrix[x][yA]
		unitB = mGraph.matrix[x][yB]
		if (unitA != "E"):
			mGraph.graph[unitA].y = yB
		if (unitB != "E"):
			mGraph.graph[unitB].y = yA
		mGraph.matrix[x][yA] = unitB
		mGraph.matrix[x][yB] = unitA
		return

	def getGraph(self):
		"Goes through all the units and adds upgrade paths to the graph.  The MGraph data structure is complete by the end of this function."
		
		self.mGraphs.append(MGraph())
		graph = self.mGraphs[0].graph
		
		for k in range(self.getNumberOfUnits()):
			unit = self.getUnitNumber(k)
			if (unit == -1):
				continue
			if (self.getUnitType(unit) not in self.exceptionList):
				graph[unit] = Node()
		
		self.getGraphEdges(graph)
		#CvUtil.pyPrint("1:\n" + str(graph))
		
		#remove units that don't upgrade to or from anything
		for unit in graph.keys():
			if (len(graph[unit].upgradesTo) == 0 and len(graph[unit].upgradesFrom) == 0):
				del(graph[unit])
		#CvUtil.pyPrint("2:\n" + str(graph))
		
		#split the graph into several disconnected graphs, filling out the rest of the data structure as we go
		mGraphIndex = 0
		while (len(self.mGraphs) > mGraphIndex):
			mGraph = self.mGraphs[mGraphIndex]
			self.mGraphs.append(MGraph())
			newMGraph = self.mGraphs[mGraphIndex + 1]
			
			#Pick a "random" element and mark it as order 0, then make all its successors higher and predecessors lower
			#We can fix that to the range (0..depth) in a moment, and we've already marked everything that's connected
			unit = mGraph.graph.iterkeys().next()
			mGraph.graph[unit].x = 0
			map = {}
			map[0] = set([unit])
			for iterlimit in range(10):
				for level in range(min(map.keys()), max(map.keys())+1):
					for unit in map[level].copy():
						node = mGraph.graph[unit]
						if (node.x != level):
							continue
						if (self.getUnitType(unit) in self.splitOutgoing):
							continue
						for u in node.upgradesTo:
							if (not mGraph.graph.has_key(u)):
								for i in range(mGraphIndex - 1, -1, -1):
									if (self.mGraphs[i].graph.has_key(u)):
										mGraph.graph[u] = Node()
										mGraph.graph[u].upgradesFrom = self.mGraphs[i].graph[u].upgradesFrom.copy()
										mGraph.graph[u].upgradesTo = self.mGraphs[i].graph[u].upgradesTo.copy()
										break
							nodeB = mGraph.graph[u]
							nodeB.x = level + 1
							if (not map.has_key(nodeB.x)):
								map[nodeB.x] = set()
							map[nodeB.x].add(u)
				for level in range (max(map.keys()), min(map.keys()) - 1, -1):
					for unit in map[level].copy():
						node = mGraph.graph[unit]
						if (node.x != level):
							continue
						if (self.getUnitType(unit) in self.splitIncoming):
							continue
						for u in node.upgradesFrom:
							if (not mGraph.graph.has_key(u)):
								for i in range(mGraphIndex - 1, -1, -1):
									if (self.mGraphs[i].graph.has_key(u)):
										mGraph.graph[u] = Node()
										mGraph.graph[u].upgradesFrom = self.mGraphs[i].graph[u].upgradesFrom.copy()
										mGraph.graph[u].upgradesTo = self.mGraphs[i].graph[u].upgradesTo.copy()
										break
							nodeB = mGraph.graph[u]
							nodeB.x = level - 1
							if (not map.has_key(nodeB.x)):
								map[nodeB.x] = set()
							map[nodeB.x].add(u)
			highOrder = max(map.keys())
			lowOrder = min(map.keys())
			map = 0
			mGraph.depth = highOrder - lowOrder + 1
						
			#Now we can move anything that isn't marked with an order to the next MGraph
			#if there's nothing to move, we're done after this iteration
			for (unit, node) in mGraph.graph.items():
				if (node.x == 999):
					newMGraph.graph[unit] = node
					del(mGraph.graph[unit])
				else:
					node.x -= lowOrder
					
			if (len(newMGraph.graph) == 0):
				del(self.mGraphs[mGraphIndex + 1])

			mGraphIndex += 1
		
		#CvUtil.pyPrint("3:\n" + str(self.mGraphs))
			
		for mGraph in self.mGraphs:
			#remove links that would otherwise have to jump 
			for (unit, node) in mGraph.graph.iteritems():
				for u in node.upgradesTo.copy():
					if (not mGraph.graph.has_key(u)):
						node.upgradesTo.remove(u)
				for u in node.upgradesFrom.copy():
					if (not mGraph.graph.has_key(u)):
						node.upgradesFrom.remove(u)
			

			nextDummy = -1
			#For any upgrade path that crosses more than one level, insert dummy nodes in between
			for (unitA, nodeA) in mGraph.graph.items():
				for unitB in nodeA.upgradesTo.copy():
					nodeB = mGraph.graph[unitB]
					if (nodeB.x - nodeA.x > 1):
						nodeA.upgradesTo.remove(unitB)
						nodeB.upgradesFrom.remove(unitA)
						n = nodeA.x + 1
						nodeA1 = nodeA # original node A
# Begin Promotions Graph fix for Warlords by Gaurav
						while (n < nodeB.x):
							nodeA.upgradesTo.add(nextDummy)
							mGraph.graph[nextDummy] = Node()
							nodeA = mGraph.graph[nextDummy]
							if n == nodeA1.x + 1:
								nodeA.upgradesFrom.add(unitA)
							else:
								nodeA.upgradesFrom.add(nextDummy + 1)
# End Promotions Graph fix for Warlords by Gaurav
							nodeA.x = n
							n += 1
							nextDummy -= 1
						nodeA.upgradesTo.add(unitB)
						nodeB.upgradesFrom.add(nextDummy + 1)
						

			#Now we can build the matrix from the order data
			#make sure the matrix is <depth> deep
			while(len(mGraph.matrix) < mGraph.depth):
				mGraph.matrix.append([])
			
			#fill out node.y and the matrix
			for (unit, node) in mGraph.graph.iteritems():
				node.y = len(mGraph.matrix[node.x])
				mGraph.matrix[node.x].append(unit)
				if (node.y >= mGraph.width):
					mGraph.width = node.y + 1

			#make all rows of the matrix the same width
			for row in mGraph.matrix:
				row.extend(["E"] * (mGraph.width - len(row)))
			
			#finally, do the Sugiyama algorithm: iteratively step through layer by layer, swapping
			#two units in layer i, if they cause fewer crosses or give a shorter line length from
			#layer i-1, then work back from the other end.  Repeat until no changes are made
			
			doneA = False
			iterlimit = 8
			while (not doneA and iterlimit > 0):
				doneA = True
				iterlimit -= 1
				for dir in [1, -1]:
					start = 1
					end = mGraph.depth
					if (dir == -1):
						start = mGraph.depth - 2
						end = -1
					for x in range(start, end, dir):
						doneB = False
						while (not doneB):
							doneB = True
							for y in range(mGraph.width - 1, 0, -1):
								medA = -1.0
								medB = -1.0
								unitA = mGraph.matrix[x][y-1]
								unitB = mGraph.matrix[x][y]
								nodeA = 0
								nodeB = 0
								setA = 0
								setB = 0
								if (unitA != "E"):
									nodeA = mGraph.graph[unitA]
									setA = nodeA.upgradesFrom
									if (dir == -1):
										setA = nodeA.upgradesTo
									medA = self.getMedianY(mGraph, setA)
								if (unitB != "E"):
									nodeB = mGraph.graph[unitB]
									setB = nodeB.upgradesFrom
									if (dir == -1):
										setB = nodeB.upgradesTo
									medB = self.getMedianY(mGraph, setB)

								if (medA < 0 and medB < 0):
									continue
								if (medA > -1 and medB > -1):
									if (medA > medB):
										self.swap(mGraph, x, y-1, y)
										doneB = False
								if (medA == -1 and medB < y):
									self.swap(mGraph, x, y-1, y)
									doneB = False
								if (medB == -1 and medA >= y):
									self.swap(mGraph, x, y-1, y)
									doneB = False
							if (doneB == False):
								doneA = False
						doneB = False
						while (not doneB):
							doneB = True
							for y in range(1, mGraph.width):
								unitA = mGraph.matrix[x][y-1]
								unitB = mGraph.matrix[x][y]
								if (unitA == "E" or unitB == "E"):
									continue
								nodeA = mGraph.graph[unitA]
								nodeB = mGraph.graph[unitB]
								setA = nodeA.upgradesFrom
								setB = nodeB.upgradesFrom
								if (dir == -1):
									setA = nodeA.upgradesTo
									setB = nodeB.upgradesTo
								crosses = 0
								crossesFlipped = 0
								for a in setA:
									yA = mGraph.graph[a].y
									for b in setB:
										yB = mGraph.graph[b].y
										if (yB < yA):
											crosses += 1
										elif (yB > yA):
											crossesFlipped += 1
								if (crossesFlipped < crosses):
									self.swap(mGraph, x, y-1, y)
									doneB = False
							if (doneB == False):
								doneA = False
						
						#this is a fix for median float->int conversions throwing off the list
						if (mGraph.matrix[x][-1] == "E"):
							sum = 0.0
							num = 0.0
							for y in range(mGraph.width - 1):
								unit = mGraph.matrix[x][y]
								if (unit != "E"):
									node = mGraph.graph[unit]
									seto = node.upgradesFrom
									if (dir == -1):
										seto = node.upgradesTo
									sum += y - self.getMedianY(mGraph, seto)
									num += 1
							if (num > 0 and sum / num < -0.5):
								for y in range(mGraph.width - 1, 0, -1):
									unit = mGraph.matrix[x][y-1]
									mGraph.matrix[x][y] = unit
									if (unit != "E"):
										mGraph.graph[unit].y = y
								mGraph.matrix[x][0] = "E"

		#CvUtil.pyPrint("4:\n" + str(self.mGraphs))
						
		#one final step: sort the graphs with the biggest one at top
		done = False
		while (done == False):
			done = True
			for i in range(1, len(self.mGraphs)):
				if (len(self.mGraphs[i-1].graph) < len(self.mGraphs[i].graph)):
					done = False
					temp = self.mGraphs[i]
					self.mGraphs[i] = self.mGraphs[i-1]
					self.mGraphs[i-1] = temp
		return
		
	################## Stuff to lay out the graph in space ###################

	def getPosition(self, x, y, verticalOffset):
		xPos = self.horizontalMargin + x * (self.buttonSize + self.horizontalSpacing)
		yPos = self.verticalMargin + y * (self.buttonSize + self.verticalSpacing) + verticalOffset
		return (xPos, yPos)
	
	def drawGraph(self):
		screen = self.pediaScreen.getScreen()
		offset = 0
		for mGraph in self.mGraphs:
			#draw arrows first so they'll go under the buttons if there is overlap
			self.drawGraphArrows(mGraph, offset)
			for x in range(mGraph.depth):
				for y in range (mGraph.width):
					unit = mGraph.matrix[x][y]
					(xPos, yPos) = self.getPosition(x, y, offset)
					if unit != "E" and unit > -1:
						self.placeOnScreen(screen, unit, xPos, yPos)
			offset = self.getPosition(0, mGraph.width, offset)[1]

	####################### Stuff to draw graph arrows #######################
	
	def drawGraphArrows(self, mGraph, offset):
		matrix = mGraph.matrix
		for x in range(len(matrix) - 1, -1, -1):
			for y in range(len(matrix[x])):
				unit = matrix[x][y]
				if unit != "E":
					self.drawUnitArrows(mGraph, offset, unit)
		return
	
	def drawUnitArrows(self, mGraph, offset, unit):
		toNode = mGraph.graph[unit]
		for fromUnit in toNode.upgradesFrom:
			fromNode = mGraph.graph[fromUnit]
			posFrom = self.getPosition(fromNode.x, fromNode.y, offset)
			posTo = self.getPosition(toNode.x, toNode.y, offset)
			self.drawArrow(posFrom, posTo, fromUnit < 0, unit < 0)
		return
	
	def drawArrow(self, posFrom, posTo, dummyFrom, dummyTo):
		screen = self.pediaScreen.getScreen()
		
		LINE_ARROW = ArtFileMgr.getInterfaceArtInfo("LINE_ARROW").getPath()
		LINE_TLBR = ArtFileMgr.getInterfaceArtInfo("LINE_TLBR").getPath()
		LINE_BLTR = ArtFileMgr.getInterfaceArtInfo("LINE_BLTR").getPath()
		LINE_STRAIT = ArtFileMgr.getInterfaceArtInfo("LINE_STRAIT").getPath()
		
		if (dummyFrom):
			xFrom = posFrom[0] + self.buttonSize / 2
		else:
			xFrom = posFrom[0] + self.buttonSize
		if (dummyTo):
			xTo = posTo[0] + self.buttonSize / 2
		else:
			xTo = posTo[0] - 8
		yFrom = posFrom[1] + (self.buttonSize / 2)
		yTo = posTo[1] + (self.buttonSize / 2)
		
		if (yFrom == yTo):
			screen.addDDSGFCAt( self.pediaScreen.getNextWidgetName(), self.upgradesList, LINE_STRAIT, xFrom, yFrom - 3, xTo - xFrom, 8, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
		else:
			xDiff = float(xTo - xFrom)
			yDiff = float(yTo - yFrom)

			iterations = int(max(xDiff, abs(yDiff)) / 80) + 1
			if (abs(xDiff/yDiff) >= 2 or abs(xDiff/yDiff) < 0.5):
				iterations = int(max(xDiff, abs(yDiff)) / 160) + 1

			line = LINE_TLBR
			if (yDiff < 0):
				line = LINE_BLTR
			for i in range(iterations):
				xF = int((xDiff / iterations) * max(i-0.1, 0)) + xFrom
				yF = int((yDiff / iterations) * max(i-0.1, 0)) + yFrom
				xT = int((xDiff / iterations) * (i + 1)) + xFrom
				yT = int((yDiff / iterations) * (i + 1)) + yFrom
				if (yT < yF):
					temp = yT
					yT = yF
					yF = temp
				screen.addDDSGFCAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, line, xF, yF, xT-xF, yT-yF, WidgetTypes.WIDGET_GENERAL, -1, -1, False)
		
		if (dummyTo == False):
			screen.addDDSGFCAt( self.pediaScreen.getNextWidgetName(), self.upgradesList, LINE_ARROW, xTo, yTo - 6, 12, 12, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
		return

########################### PROMOTION GRAPH IMPLEMENTATION #############################

#The promotion graph works exactly like the unit upgrade graph.  Just a few functions need to
#be changed to make it access promotions instead of unit infos.  These functions do that.
#This is a subclass inherited directly from UnitUpgradesGraph, so all the functions that are
#not listed here are above.

class PromotionsGraph(UnitUpgradesGraph):

	def __init__(self, pediaScreen):
		self.mGraphs = []
		self.horizontalMargin = promotionsHorizontalMargin
		self.verticalMargin = promotionsVerticalMargin
		self.horizontalSpacing = promotionsHorizontalSpacing
		self.verticalSpacing = promotionsVerticalSpacing
		self.pediaScreen = pediaScreen
		self.upgradesList = pediaScreen.UPGRADES_GRAPH_ID
		self.buttonSize = promotionsButtonSize
		self.exceptionList = promotionsExceptionList
		self.splitIncoming = promotionsSplitIncoming
		self.splitOutgoing = promotionsSplitOutgoing

	def getNumberOfUnits(self):
		return gc.getNumPromotionInfos()

	def getUnitNumber(self, k):
		"Gets the id for the kth unit for the current active player"
		
		# No unique promotions, so very simple
		return k

	def getUnitType(self, e):
		"Returns the type of the units with the specified id"
		return gc.getPromotionInfo(e).getType()

	def getGraphEdges(self, graph):
		for unitA in graph.iterkeys():
			unitD = gc.getPromotionInfo(unitA).getPrereqPromotion()
			self.addUpgradePath(graph, unitD, unitA)
			unitB = gc.getPromotionInfo(unitA).getPrereqOrPromotion1()
			self.addUpgradePath(graph, unitB, unitA)
			unitC = gc.getPromotionInfo(unitA).getPrereqOrPromotion2()
			self.addUpgradePath(graph, unitC, unitA)
		
	def unitToString(self, unit):
		return gc.getPromotionInfo(unit).getDescription() + ":%d"%(unit, )


	def placeOnScreen(self, screen, unit, xPos, yPos):
		screen.setImageButtonAt(self.pediaScreen.getNextWidgetName(), self.upgradesList, gc.getPromotionInfo(unit).getButton(), xPos, yPos, self.buttonSize, self.buttonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, unit, 1)
