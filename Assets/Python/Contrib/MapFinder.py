## MapGenerator
##
## Shortcut to regenerate the map and start/stop HOF's MapFinder utility.
##
## Shortcuts:
##
##   ALT + G                   doRegenerate()
##   ALT + CTRL + G	           doStart()
##   ALT + CTRL + SHIFT + G    doStop()
##
## Adapted from HOF Mod 3.13.001.
##
## Notes
##   - May be initialized externally by calling init()
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: HOF Team, EmperorFool

from CvPythonExtensions import *
import AutoSave
import BugCore
import BugDll
import BugUtil
import MapFinderStatusScreen
import os.path

MINIMUM_SAVE_DELAY = 2.0

gc = CyGlobalContext()
options = BugCore.game.MapFinder


# Initialization

def init(minimumSaveDelay=0.0):
	"""
	Allows config XML to set the minimum delay.
	"""
	global MINIMUM_SAVE_DELAY
	MINIMUM_SAVE_DELAY = minimumSaveDelay


# Regenerate Map

def doRegenerate(argsList=None):
	try:
		regenerate()
	except MapFinderError, e:
		e.display()

def canRegenerate():
	enforceDll()
	if gc.getGame().canRegenerateMap():
		return True
	else:
		raise MapFinderError("TXT_KEY_MAPFINDER_CANNOT_REGENERATE")

def regenerate():
	if canRegenerate():
		if CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_SHOW:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_SHOW)
		BugUtil.alert(BugUtil.getPlainText("TXT_KEY_MAPFINDER_REGNERATING"))
		# must defer to allow alert to appear
		BugUtil.deferCall(regenerateForReal)

def regenerateForReal():
	if not gc.getGame().regenerateMap():
		raise MapFinderError("TXT_KEY_MAPFINDER_REGENERATE_FAILED")
	# must defer to allow screen to update before moving camera
	BugUtil.deferCall(centerCameraOnPlayer)

def centerCameraOnPlayer():
	cam = CyCamera()
	eSpeed = cam.GetCameraMovementSpeed()
	cam.SetCameraMovementSpeed(CameraMovementSpeeds.CAMERAMOVEMENTSPEED_FAST)
	plot = gc.getActivePlayer().getStartingPlot()
	cam.JustLookAtPlot(plot)
	cam.SetCameraMovementSpeed(eSpeed)


# Regeneration Loop

(
	NO_FEATURE,
	FEATURE_ICE,
	FEATURE_JUNGLE,
	FEATURE_OASIS,
	FEATURE_FLOOD_PLAINS,
	FEATURE_FOREST,
	FEATURE_FALLOUT,
) = range(-1, 6)
FEATURE_LAKE = 99

(
	NO_TERRAIN,
	TERRAIN_GRASS,
	TERRAIN_PLAINS,
	TERRAIN_DESERT,
	TERRAIN_TUNDRA,
	TERRAIN_SNOW,
	TERRAIN_COAST,
	TERRAIN_OCEAN,
	TERRAIN_PEAK,
	TERRAIN_HILL,
) = range(-1, 9)

CODES_BY_TYPES = {  # BasicPlot_CodeToTypes
	('water', TERRAIN_OCEAN, NO_FEATURE) : 401,
	('water', TERRAIN_COAST, FEATURE_ICE) : 402,
	('land', TERRAIN_DESERT, NO_FEATURE) : 403,
	('hills', TERRAIN_DESERT, NO_FEATURE) : 404,
	('land', TERRAIN_DESERT, FEATURE_FLOOD_PLAINS) : 405,
	('land', TERRAIN_GRASS, NO_FEATURE) : 406,
	('land', TERRAIN_GRASS, FEATURE_FOREST) : 407,
	('hills', TERRAIN_GRASS, NO_FEATURE) : 408,
	('hills', TERRAIN_GRASS, FEATURE_FOREST) : 409,
	('hills', TERRAIN_GRASS, FEATURE_JUNGLE) : 410,
	('land', TERRAIN_GRASS, FEATURE_JUNGLE) : 411,
	('land', TERRAIN_DESERT, FEATURE_OASIS) : 412,
	('water', TERRAIN_OCEAN, FEATURE_ICE) : 413,
	('peak', TERRAIN_PEAK, NO_FEATURE) : 414,
	('land', TERRAIN_PLAINS, NO_FEATURE) : 415,
	('land', TERRAIN_PLAINS, FEATURE_FOREST) : 416,
	('hills', TERRAIN_PLAINS, NO_FEATURE) : 417,
	('hills', TERRAIN_PLAINS, FEATURE_FOREST) : 418,
	('water', TERRAIN_COAST, NO_FEATURE) : 419,
	('land', TERRAIN_SNOW, NO_FEATURE) : 420,
	('land', TERRAIN_SNOW, FEATURE_FOREST) : 421,
	('hills', TERRAIN_SNOW, NO_FEATURE) : 422,
	('hills', TERRAIN_SNOW, FEATURE_FOREST) : 423,
	('land', TERRAIN_TUNDRA, NO_FEATURE) : 424,
	('land', TERRAIN_TUNDRA, FEATURE_FOREST) : 425,
	('hills', TERRAIN_TUNDRA, NO_FEATURE) : 426,
	('hills', TERRAIN_TUNDRA, FEATURE_FOREST) : 427,
	('water', TERRAIN_COAST, FEATURE_LAKE) : 428,
}

# unused
TYPES_BY_CODE = {  # BasicPlot_TypesToCode
	401 : ('water', TERRAIN_OCEAN, NO_FEATURE),
	402 : ('water', TERRAIN_COAST, FEATURE_ICE),
	403 : ('land', TERRAIN_DESERT, NO_FEATURE),
	404 : ('hills', TERRAIN_DESERT, NO_FEATURE),
	405 : ('land', TERRAIN_DESERT, FEATURE_FLOOD_PLAINS),
	406 : ('land', TERRAIN_GRASS, NO_FEATURE),
	407 : ('land', TERRAIN_GRASS, FEATURE_FOREST),
	408 : ('hills', TERRAIN_GRASS, NO_FEATURE),
	409 : ('hills', TERRAIN_GRASS, FEATURE_FOREST),
	410 : ('hills', TERRAIN_GRASS, FEATURE_JUNGLE),
	411 : ('land', TERRAIN_GRASS, FEATURE_JUNGLE),
	412 : ('land', TERRAIN_DESERT, FEATURE_OASIS),
	413 : ('water', TERRAIN_OCEAN, FEATURE_ICE),
	414 : ('peak', TERRAIN_PEAK, NO_FEATURE),
	415 : ('land', TERRAIN_PLAINS, NO_FEATURE),
	416 : ('land', TERRAIN_PLAINS, FEATURE_FOREST),
	417 : ('hills', TERRAIN_PLAINS, NO_FEATURE),
	418 : ('hills', TERRAIN_PLAINS, FEATURE_FOREST),
	419 : ('water', TERRAIN_COAST, NO_FEATURE),
	420 : ('land', TERRAIN_SNOW, NO_FEATURE),
	421 : ('land', TERRAIN_SNOW, FEATURE_FOREST),
	422 : ('hills', TERRAIN_SNOW, NO_FEATURE),
	423 : ('hills', TERRAIN_SNOW, FEATURE_FOREST),
	424 : ('land', TERRAIN_TUNDRA, NO_FEATURE),
	425 : ('land', TERRAIN_TUNDRA, FEATURE_FOREST),
	426 : ('hills', TERRAIN_TUNDRA, NO_FEATURE),
	427 : ('hills', TERRAIN_TUNDRA, FEATURE_FOREST),
	428 : ('water', TERRAIN_COAST, FEATURE_LAKE),
}

bActive = False
savedInterfaceMode = None

iRegenCount = 0
iSavedCount = 0

def isActive():
	return bActive

def doStart(argsList=None):
	try:
		if not bActive:
			start()
		else:
			BugUtil.alert(BugUtil.getPlainText("TXT_KEY_MAPFINDER_ALREADY_RUNNING"))
	except MapFinderError, e:
		MapFinderStatusScreen.hide()
		e.display()

def doStop(argsList=None):
	try:
		if bActive:
			stop()
		else:
			BugUtil.alert(BugUtil.getPlainText("TXT_KEY_MAPFINDER_NOT_RUNNING"))
	except MapFinderError, e:
		e.display()

def start():
	if canRegenerate():
		setup()
		MapFinderStatusScreen.show()
		global bActive, iRegenCount, iSavedCount
		bActive = True
		iRegenCount = 0
		iSavedCount = 0
		showInterface()
		finderStartLoop()

def stop():
	global bActive
	bActive = False
	MapFinderStatusScreen.hide()
	restoreInterface()
	BugUtil.alert(BugUtil.getPlainText("TXT_KEY_MAPFINDER_STOPPED") + " - " + getCountsText())

def showInterface():
	global savedInterfaceMode
	if not savedInterfaceMode:
		savedInterfaceMode = CyInterface().getShowInterface()
	CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_SHOW)

def restoreInterface():
	global savedInterfaceMode
	if savedInterfaceMode:
		CyInterface().setShowInterface(savedInterfaceMode)

def getCountsText():
	return (u"%s %d, %s %d" % 
			(BugUtil.getPlainText("TXT_KEY_MAPFINDER_TOTAL_MAPS"), iRegenCount, 
			 BugUtil.getPlainText("TXT_KEY_MAPFINDER_TOTAL_SAVES"), iSavedCount))


def finderStartLoop():
	BugUtil.deferCall(finderCanRegenerate, options.getRegenerationDelay())

def finderCanRegenerate():
	if bActive:
		try:
			if canRegenerate():
				MapFinderStatusScreen.setStatus(BugUtil.getPlainText("TXT_KEY_MAPFINDER_REGNERATING"))
				# must defer to allow screen to update
				BugUtil.deferCall(finderRegenerate)
		except MapFinderError, e:
			e.display()
			stop()

def finderRegenerate():
	if bActive:
		try:
			if not gc.getGame().regenerateMap():
				raise MapFinderError("TXT_KEY_MAPFINDER_REGENERATE_FAILED")
			# must defer to allow screen to update before moving camera
			BugUtil.deferCall(finderCheck)
		except MapFinderError, e:
			e.display()
			stop()

def finderCheck():
	centerCameraOnPlayer()
	if bActive:
		global iRegenCount
		iRegenCount += 1
		MapFinderStatusScreen.update()
		if matchRules():
			finderSave()
		else:
			finderNext()

def finderSave():
	MapFinderStatusScreen.setStatus(BugUtil.getPlainText("TXT_KEY_MAPFINDER_SAVING"))
	# must delay long enough to allow unrevealed tiles to disappear before taking the screenshot
	delay = options.getSaveDelay()
	if delay < MINIMUM_SAVE_DELAY:
		delay = MINIMUM_SAVE_DELAY
	BugUtil.deferCall(save, delay)

def finderNext():
	MapFinderStatusScreen.resetStatus()
	BugUtil.deferCall(next, options.getSkipDelay())

def next():
	if bActive:
		if ((iRegenCount >= options.getRegenerationLimit()) or
			(iSavedCount >= options.getSaveLimit())):
			stop()
		else:
#			BugUtil.alert("MapFinder running - Count %d, Saved %d", iRegenCount, iSavedCount)
			finderStartLoop()


mr = None
def matchRules():
	global mr
	mr = {}
	for x in CodeText.iterkeys():
		mr[x] = 0

	iActivePlayer = gc.getGame().getActivePlayer()
	activePlayer = gc.getPlayer(iActivePlayer)
	iTeam = activePlayer.getTeam()

	startplot = activePlayer.getStartingPlot()
	iStartX = startplot.getX()
	iStartY = startplot.getY()
	iMaxX = gc.getMap().getGridWidth()
	iMaxY = gc.getMap().getGridHeight()
	bWrapX = gc.getMap().isWrapX()
	bWrapY = gc.getMap().isWrapY()

	lX = {}
	lY = {}
	if (Rules['Range'] != 999):

		lMax = (Rules['Range'] * 2) + 1
		iX = iStartX - Rules['Range']
		if (iX < 0):
			if (bWrapX):
				iX = iMaxX + iX
			else:
				iX = 0
		for i in range(1, lMax + 1):
			lX[i] = iX
			iX = iX + 1
			if iX > iMaxX: 0
			if iX < 0: iMaxX

		iY = iStartY - Rules['Range']
		if (iY < 0):
			if (bWrapY):
				iY = iMaxY + iY
			else:
				iY = 0
		for i in range(1, lMax + 1):
			lY[i] = iY
## HOF MOD V1.61.005
##			iy = iX + 1
			iY = iY + 1
## end HOF MOD V1.61.005
			if iY > iMaxY: 0
			if iY < 0: iMaxY
			
##	displayMsg(str(lX.values()) + "\n" + str(lY.values()))

	for iY in range(0, iMaxY):
		for iX in range(0, iMaxX):

			if (Rules['Range'] != 999):
## HOF MOD V1.61.005
				# skip if outside range
				if iX not in lX.values(): continue
				if iY not in lY.values(): continue
				# use fat-cross if over 1 range
				if  (Rules['Range'] > 1):
					# fat cross, skip diagonal corners
					if (iX == lX[1] and iY == lY[1]): continue
					if (iX == lX[1] and iY == lY[lMax]): continue
					if (iX == lX[lMax] and iY == lY[1]): continue
					if (iX == lX[lMax] and iY == lY[lMax]): continue
## end HOF MOD V1.61.005
##			displayMsg(str(iX) + "/" + str(iY))
			
			plot = gc.getMap().plot(iX, iY)
			if (plot.isRevealed(iTeam, False)):
				
				if (plot.isFlatlands()): p = 'land'
				elif (plot.isWater()): p = 'water'
				elif (plot.isHills()): p = 'hills'
				elif (plot.isPeak()): p = 'peak'
				t = plot.getTerrainType()
				if (plot.isLake()):
					f = FEATURE_LAKE
				else:
					f = plot.getFeatureType()
				ip = -1
				if CODES_BY_TYPES.has_key((p, t, f)):
					ip = CODES_BY_TYPES[(p, t, f)]
					mr[ip] = mr[ip] + 1
					for k, l in Category_Types.iteritems():
						if (ip in l): mr[k] = mr[k] + 1

				ib = plot.getBonusType(iTeam) + 500
				if mr.has_key(ib):
					mr[ib] = mr[ib] + 1
					for k, l in Category_Types.iteritems():
						if (ib in l): mr[k] = mr[k] + 1

				# Base Commerce
				xc = plot.calculateYield(YieldTypes.YIELD_COMMERCE, True)
				mr[301] = mr[301] + xc
				# Base Food
				xf = plot.calculateYield(YieldTypes.YIELD_FOOD, True)
				mr[302] = mr[302] + xf
				# Extra Base Food
				if (xf > 2): mr[310] = mr[310] + (xf - 2)
				# Base Production
				xp = plot.calculateYield(YieldTypes.YIELD_PRODUCTION, True)
				mr[303] = mr[303] + xp
				
				if (plot.isGoody()): mr[601] = mr[601] + 1
				
## HOF MOD V1.61.005
				if Combo_Types.has_key((ib, ip)):
					ic = Combo_Types[(ib, ip)]
					if mr.has_key(ic):
						mr[ic] = mr[ic] + 1
						
				# Starting Plot?
				if iX == iStartX and iY == iStartY:
					if Combo_Types.has_key((999, ip)):
						ic = Combo_Types[(999, ip)]
						if mr.has_key(ic):
							mr[ic] = mr[ic] + 1

				if (plot.isRiver()):
					mr[602] = mr[602] + 1
					ipr = ip + 50
					if mr.has_key(ipr):
						mr[ipr] = mr[ipr] + 1
					if Combo_Types.has_key((ib, ipr)):
						ic = Combo_Types[(ib, ipr)]
						if mr.has_key(ic):
							mr[ic] = mr[ic] + 1
					# Starting Plot?
					if iX == iStartX and iY == iStartY:
						if Combo_Types.has_key((999, ipr)):
							ic = Combo_Types[(999, ipr)]
							if mr.has_key(ic):
								mr[ic] = mr[ic] + 1

				if (plot.isFreshWater()):
					mr[603] = mr[603] + 1
					ipf = ip + 150
					if mr.has_key(ipf):
						mr[ipf] = mr[ipf] + 1
					if Combo_Types.has_key((ib, ipf)):
						ic = Combo_Types[(ib, ipf)]
						if mr.has_key(ic):
							mr[ic] = mr[ic] + 1
					# Starting Plot?
					if iX == iStartX and iY == iStartY:
						if Combo_Types.has_key((999, ipf)):
							ic = Combo_Types[(999, ipf)]
							if mr.has_key(ic):
								mr[ic] = mr[ic] + 1
## end HOF MOD V1.61.005

	lPF = []
	for g, r in Rules.iteritems():
		if (g == 'Range'): continue
		grp = True
		for k, v in r.iteritems():
			if (mr.has_key(k)):
				if ((v[1] == 0 and mr[k] != 0) or (mr[k] < v[0]) or (mr[k] > v[1])):
					grp = False
					break
			else:
				grp = False
				break

		lPF.append(grp)

	for i in range(len(lPF)):
		if (lPF[i]):
			return True
	return False

def save():
	global iRegenCount, iSavedCount, mr
	iSavedCount += 1
	sMFSavePath = options.getSavePath()
	(fileName, _) = AutoSave.getSaveFileName(sMFSavePath)
	fullFileName = fileName + "_" + str(iRegenCount) + "_" + str(iSavedCount)
	
	# screenshot
	screenFile = fullFileName + ".jpg"
	gc.getGame().takeJPEGScreenShot(screenFile)
	
	# report file
	reportFile = fullFileName + ".txt"
	file = open(reportFile, "a")
	ruleFile = options.getRuleFile()

## HOF MOD V1.61.005
	# don't change unless file format changes!
	file.write("HOF MOD V1.61.004,HOF MOD V1.61.005,\n")
## end HOF MOD V1.61.005

	file.write("Name,Name," + str(fileName) + "_" + str(iRegenCount) + "_" + str(iSavedCount) + "\n")
	file.write("Rule File,Rule File," + str(ruleFile) + "\n")
	file.write("Range,Range," + str(Rules['Range']) + "\n")

	lKeys = mr.keys()
	lKeys.sort()
	for x in lKeys:
		if (x < 900):
			file.write(str(x) + "," + str(CodeText[x]) + "," + str(mr[x]) + "\n")
	file.close()

	# saved game
	saveFile = fullFileName + ".CivBeyondSwordSave"
	gc.getGame().saveGame(saveFile)
	
	MapFinderStatusScreen.update()
	MapFinderStatusScreen.resetStatus()
	next()


def setup():
	root = options.getPath()
	if not os.path.isdir(root):
		raise MapFinderError("TXT_KEY_MAPFINDER_INVALID_PATH", root)
	saves = options.getSavePath()
	if not os.path.isdir(saves):
		raise MapFinderError("TXT_KEY_MAPFINDER_INVALID_SAVE_PATH", saves)
	loadCodeText(root)
	loadCategoryTypes(root)
	loadComboTypes(root)
	loadRuleSet(root)

def findSystemFile(root, file):
	path = os.path.join(root, file)
	if not os.path.isfile(path):
		raise MapFinderError("TXT_KEY_MAPFINDER_INVALID_SYSTEM_FILE", file)
	return path

def loadCodeText(root):
	global CodeText
	lLang = []
	CodeText = {}
	iLang = gc.getGame().getCurrentLanguage()
	path = findSystemFile(root, 'MF_Text.dat')
	file = open(path, "r")
	for temp in file:
		(sCat, sCode, sLang0, sLang1, sLang2, sLang3, sLang4) = temp.split(",")
		iCat = int(sCat.strip())
		iCode = int(sCode.strip())
		lLang = [sLang0.strip(), sLang1.strip(), sLang2.strip(),
					sLang3.strip(), sLang4.strip()]
		CodeText[iCode] = lLang[iLang]
	file.close()
	file = None

def loadCategoryTypes(root):
	global Category_Types
	Category_Types = {}
	path = findSystemFile(root, 'MF_Cat_Rules.dat')
	file = open(path, "r")
	iCatSave = -1
	for temp in file:
		(sCat, sRule) = temp.split(",")
		iCat = int(sCat.strip())
		iRule = int(sRule.strip())
		if (iCat != iCatSave):
			Category_Types[iCat] = (iRule,)
		else:
			Category_Types[iCat] = Category_Types[iCat] + (iRule,)

		iCatSave = iCat
	file.close()
	file = None

def loadComboTypes(root):
	global Combo_Types
	Combo_Types = {}
	path = findSystemFile(root, 'MF_Combo_Rules.dat')
	file = open(path, "r")
	for temp in file:
		(sCat, sBonus, sTerrain) = temp.split(",")
		iCat = int(sCat.strip())
		iBonus = int(sBonus.strip())
		iTerrain = int(sTerrain.strip())
		Combo_Types[(iBonus, iTerrain)] = iCat
	file.close()
	file = None

def loadRuleSet(root):
	global Rules
	Rules = {}
	Rules['Range'] = 2
	path = os.path.join(root, "Rules", options.getRuleFile())
	if not os.path.isfile(path):
		raise MapFinderError("Invalid MapFinder rule file: %s", options.getRuleFile())
	iGrpSave = 0
	Rules = {}
	file = open(path, "r")
	for temp in file:
		(sGrp, sCat, sRule, sMin, sMax) = temp.split(",")
		iGrp = int(sGrp.strip())
		iCat = int(sCat.strip())
		if (iGrp == 0):
			Rules['Range'] = iCat
		else:
			iRule = int(sRule.strip())
			iMin = int(sMin.strip())
			iMax = int(sMax.strip())
			if (iGrp != iGrpSave):
				Rules[iGrp] = {iRule : (iMin, iMax)}
			else:
				Rules[iGrp][iRule] = (iMin, iMax)
		iGrpSave = iGrp
	file.close()
	file = None


# common utility functions

def enforceDll():
	if not BugDll.isPresent():
		raise MapFinderError("TXT_KEY_MAPFINDER_REQUIRES_BULL")

class MapFinderError:
	def __init__(self, key, *args):
		self.key = key
		self.args = args
	def display(self):
		BugUtil.error(BugUtil.getText(self.key, self.args))
