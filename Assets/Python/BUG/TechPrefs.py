## TechPrefs
##
## Builds ordered lists of techs as preferred by the various Great People.
##
## Copyright (c) 2007-2008 The BUG Mod.
##
## Author: EmperorFool

from CvPythonExtensions import *

# BUG - Mac Support - start
import BugUtil
BugUtil.fixSets(globals())
# BUG - Mac Support - end

gc = CyGlobalContext()

# see gc.getNumFlavorTypes() and gc.getFlavorTypes()
# not available via gc.getInfoTypeForString(), thus the hard-coding here :(
NUM_FLAVORS = 8
FLAVORS = [ "Military", "Religion", "Production",
			"Gold", "Science", "Culture",
			"Growth", "Espionage" ]
(
	FLAVOR_MILITARY,
	FLAVOR_RELIGION,
	FLAVOR_PRODUCTION,
	FLAVOR_GOLD,
	FLAVOR_SCIENCE,
	FLAVOR_CULTURE,
	FLAVOR_GROWTH,
	FLAVOR_ESPIONAGE,
) = range(NUM_FLAVORS)

class TechPrefs:

	def __init__(self):
		self.NUM_TECHS = gc.getNumTechInfos()
		self.NUM_AND_PREREQS = gc.getDefineINT("NUM_AND_TECH_PREREQS")
		self.NUM_OR_PREREQS = gc.getDefineINT("NUM_OR_TECH_PREREQS")
		
		self.mTechs = {}
		self.lTechsByFlavor = []
		for iFlavor in range(NUM_FLAVORS):
			self.lTechsByFlavor.append([])
		
		# build a list of all techs and a list of techs for each flavor
		for iTech in range(self.NUM_TECHS):
			pTechInfo = gc.getTechInfo(iTech)
			pTech = self.getTech(iTech)
			for iFlavor in range(NUM_FLAVORS):
				iFlavorValue = pTechInfo.getFlavorValue(iFlavor)
				if (iFlavorValue > 0):
					pTech.setFlavorValue(iFlavor, iFlavorValue)
					self.lTechsByFlavor[iFlavor].append((-iFlavorValue, iTech, pTech))
					bHasFlavor = True
			
			# hook up prereq techs
			for i in range(self.NUM_AND_PREREQS):
				pPrereqTech = pTechInfo.getPrereqAndTechs(i)
				if (pPrereqTech != -1):
					pTech.addAndPrereq(self.getTech(pPrereqTech))
			for i in range(self.NUM_OR_PREREQS):
				pPrereqTech = pTechInfo.getPrereqOrTechs(i)
				if (pPrereqTech != -1):
					pTech.addOrPrereq(self.getTech(pPrereqTech))
		
		# sort each flavor's list of techs by decreasing preference: reverse flavor value, tech number
		# and create a copy that doesn't get trimmed as techs are researched
		self.lAllTechsByFlavor = {}
		for iFlavor in range(NUM_FLAVORS):
			lTechs = self.lTechsByFlavor[iFlavor]
##			print "%s has %d techs" % (FLAVORS[iFlavor], len(lTechs))
			lTechs.sort()
			self.lTechsByFlavor[iFlavor] = [ pTech for _, _, pTech in lTechs ]
			self.lAllTechsByFlavor[iFlavor] = tuple(self.lTechsByFlavor[iFlavor])
		
##		print "---- Techs with Flavor ----"
##		for pTech in self.mTechs.values():
##			print "%2d: %s" % (pTech.iTech, pTech.getName())
##		for iFlavor in range(NUM_FLAVORS):
##			print "---- %d Techs with Flavor %s ----" % (len(self.lTechsByFlavor[iFlavor]), FLAVORS[iFlavor])
##			for pTech in self.lTechsByFlavor[iFlavor]:
##				print "%2d-%2d: %s" % (pTech.getFlavorValue(iFlavor), pTech.iTech, pTech.getName())
		
##		pOptics = self.getTech(gc.getInfoTypeForString("TECH_OPTICS"))
##		print pOptics
##		pAstronomy = self.getTech(gc.getInfoTypeForString("TECH_ASTRONOMY"))
##		print pAstronomy
##		pPhysics = self.getTech(gc.getInfoTypeForString("TECH_PHYSICS"))
##		print pPhysics
##		pAstronomy.removeFromTree()
##		print pOptics
##		print pAstronomy
##		print pPhysics
##		
##		self.removeKnownTechs()
##		print self.getNextResearchableFlavorTech(FLAVOR_RELIGION)
##		print self.getNextResearchableFlavorTech(FLAVOR_SCIENCE)
##		print self.getNextResearchableFlavorTech(FLAVOR_GOLD)
##		techs = set()
##		techs.add(self.getTechStr("TECH_THE_WHEEL"))
##		techs.add(self.getTechStr("TECH_MYSTICISM"))
##		print self.getNextResearchableWithFlavorTech(FLAVOR_RELIGION, techs)
##		print self.getNextResearchableWithFlavorTech(FLAVOR_SCIENCE, techs)
##		print self.getNextResearchableWithFlavorTech(FLAVOR_GOLD, techs)
##		techs.add(self.getTechStr("TECH_IRON_WORKING"))
##		techs.add(self.getTechStr("TECH_IRON_POTTERY"))
##		techs.add(self.getTechStr("TECH_MEDITATION"))
##		print self.getNextResearchableWithFlavorTech(FLAVOR_RELIGION, techs)
##		print self.getNextResearchableWithFlavorTech(FLAVOR_SCIENCE, techs)
##		print self.getNextResearchableWithFlavorTech(FLAVOR_GOLD, techs)#


	def getTech(self, iTech):
		if iTech not in self.mTechs:
			self.mTechs[iTech] = Tech(iTech)
		return self.mTechs[iTech]

	def getTechStr(self, sTech):
		iTech = gc.getInfoTypeForString(sTech)
		if iTech in self.mTechs:
			return self.mTechs[iTech]
		return None

	def removeTech(self, iTech):
		"""Removes the given tech, usually because it has been researched."""
		if (iTech in self.mTechs):
			pTech = self.mTechs[iTech]
			del self.mTechs[iTech]
			for iFlavor in range(NUM_FLAVORS):
				if pTech in self.lTechsByFlavor[iFlavor]:
					self.lTechsByFlavor[iFlavor].remove(pTech)
			pTech.removeFromTree()

	def removeKnownTechs(self):
		"""Removes the techs known to the current team."""
		pTeam = gc.getTeam(gc.getActivePlayer().getTeam())
		for iTech in range(self.NUM_TECHS):
			if (pTeam.isHasTech(iTech)):
				self.removeTech(iTech)


	def getResearchableTechs(self):
		"""Returns a set of all techs that can be researched now."""
		sCan = set()
		for pTech in self.mTechs.values():
			if (pTech.canResearch()):
				sCan.add(pTech)
		return sCan

	def getResearchableWithTechs(self, sTechs):
		"""Returns a set of all techs that can be researched once the given techs have been researched."""
		sCan = set()
		for pTech in self.mTechs.values():
			if (pTech not in sTechs and pTech.canResearchWith(sTechs)):
				sCan.add(pTech)
		return sCan


	def getNextFlavorTech(self, iFlavor):
		"""Returns the next tech in the flavor's list or None."""
		if (len(self.lTechsByFlavor[iFlavor]) > 0):
			return self.lTechsByFlavor[iFlavor][0]
		else:
			return None

	def getNextResearchableFlavorTech(self, iFlavor):
		"""Returns the next tech in the flavor's list that is researchable now or None."""
		for pTech in self.lTechsByFlavor[iFlavor]:
			if (pTech.canResearch()):
				return pTech
		return None

	def getNextResearchableWithFlavorTech(self, iFlavor, sTechs):
		"""Returns the next tech in the flavor's list that is researchable once the given techs are researched or None."""
		for pTech in self.lTechsByFlavor[iFlavor]:
			if (pTech not in sTechs and pTech.canResearchWith(sTechs)):
				return pTech
		return None

	def getAllFlavorTechs(self, iFlavor):
		"""Returns a list of all techs in the flavor's list."""
		lTechs = []
		for pTech in self.lAllTechsByFlavor[iFlavor]:
			lTechs.append(pTech)
		return lTechs

	def getCurrentFlavorTechs(self, iFlavor):
		"""Returns a list of techs in the flavor's list that are researchable now."""
		lTechs = []
		for pTech in self.lTechsByFlavor[iFlavor]:
			if (pTech.canResearch()):
				lTechs.append(pTech)
		return lTechs

	def getCurrentWithFlavorTechs(self, iFlavor, sTechs):
		"""Returns a list of techs in the flavor's list that are researchable once sTechs have been researched."""
		lTechs = []
		for pTech in self.lTechsByFlavor[iFlavor]:
			if (pTech not in sTechs and pTech.canResearchWith(sTechs)):
				lTechs.append(pTech)
		return lTechs

	def getRemainingFlavorTechs(self, iFlavor):
		"""Returns a list of techs in the flavor's list that haven't been researched yet."""
		lTechs = []
		for pTech in self.lTechsByFlavor[iFlavor]:
			if (pTech.getID() in self.mTechs):
				lTechs.append(pTech)
		return lTechs

	def getFutureFlavorTechs(self, iFlavor, sTechs):
		"""Returns a list of techs in the flavor's list that haven't been researched yet and aren't in <sTechs>."""
		lTechs = []
		for pTech in self.lTechsByFlavor[iFlavor]:
			if (pTech.getID() in self.mTechs and pTech not in sTechs):
				lTechs.append(pTech)
		return lTechs


	def printFlavorTechs(self, iFlavor):
		"""Prints the techs in the flavor's list."""
		for pTech in self.lTechsByFlavor[iFlavor]:
			print pTech

	def printResearchableFlavorTechs(self, iFlavor):
		"""Prints the techs in the flavor's list."""
		for pTech in self.lTechsByFlavor[iFlavor]:
			if pTech.canResearch():
				print pTech

	def printResearchableWithFlavorTechs(self, iFlavor, sTechs):
		"""Prints the techs in the flavor's list."""
		for pTech in self.lTechsByFlavor[iFlavor]:
			if pTech.canResearchWith(sTechs):
				print pTech


class Tech:
	
	def __init__(self, iTech):
		self.iTech = iTech
		self.lFlavorValues = [0] * NUM_FLAVORS
		self.lFlavorPref = [0] * NUM_FLAVORS
		self.sAndPrereqs = set()
		self.sOrPrereqs = set()
		self.iNumAndPrereqs = 0
		self.iNumOrPrereqs = 0
		self.sLeadsTo = set()

	def getID(self):
		return self.iTech

	def getInfo(self):
		return gc.getTechInfo(self.iTech)

	def getName(self):
		return self.getInfo().getDescription()
	
	def __hash__(self):
		return hash(self.iTech)
	
	def __eq__(self, other):
		return self.iTech == other.iTech
	
	def __cmp__(self, other):
		return self.iTech - other.iTech


	def setFlavorValue(self, iFlavor, iValue):
		self.lFlavorValues[iFlavor] = iValue

	def getFlavorValue(self, iFlavor):
		return self.lFlavorValues[iFlavor]

	def setFlavorPref(self, iFlavor, iPref):
		self.lFlavorPref[iFlavor] = iPref

	def getFlavorPref(self, iFlavor):
		return self.lFlavorPref[iFlavor]


	def addAndPrereq(self, pTech):
		if pTech not in self.sAndPrereqs:
			self.iNumAndPrereqs += 1
			self.sAndPrereqs.add(pTech)
			pTech.addLeadsTo(self)

	def addOrPrereq(self, pTech):
		if pTech not in self.sOrPrereqs:
			self.iNumOrPrereqs += 1
			self.sOrPrereqs.add(pTech)
			pTech.addLeadsTo(self)

	def removePrereq(self, pTech):
		self.sAndPrereqs.discard(pTech)
		self.sOrPrereqs.discard(pTech)


	def getNumTechsNeeded(self):
		"""Returns the minimum number of techs that must be researched to be able to research this tech."""
		return self.getNumAndTechsNeeded() + self.getNumOrTechsNeeded()

	def getNumAndTechsNeeded(self):
		return len(self.sAndPrereqs)

	def getNumOrTechsNeeded(self):
		if (len(self.sOrPrereqs) == 0 or len(self.sOrPrereqs) < self.iNumOrPrereqs):
			return 0
		return 1

	def getTechsNeeded(self):
		"""
		Returns two sets of techs that are needed to make this tech researchable.
		
		The first set are all missing And prereqs.
		The second set is all Or prereqs or an empty set if at least one has already been researched.
		"""
		andSet = self.sAndPrereqs.copy()
		if (len(self.sOrPrereqs) == 0 or len(self.sOrPrereqs) < self.iNumOrPrereqs):
			orSet = set()
		else:
			orSet = self.sOrPrereqs.copy()
		return andSet, orSet

	def canResearch(self):
		"""Returns True if this tech has met all And prereqs and at least one Or prereq."""
		return self.getNumTechsNeeded() == 0

	def canResearchWith(self, sTechs):
		"""Returns True if this tech can be researched once the given tech(s) have been researched."""
		if (len(sTechs) == 0):
			return self.canResearch()
		sAnds = self.sAndPrereqs.difference(sTechs)
		sOrs = self.sOrPrereqs.difference(sTechs)
		return (len(sOrs) == 0 or len(sOrs) < self.iNumOrPrereqs) and len(sAnds) == 0


	def addLeadsTo(self, pTech):
		self.sLeadsTo.add(pTech)

	def removeLeadsTo(self, pTech):
		self.sLeadsTo.discard(pTech)

	def removeFromTree(self):
		"""Removes this tech from the prereq lists of the techs it leads to and the leads to lists of its prereqs."""
		for pTech in self.sAndPrereqs:
			pTech.removeLeadsTo(self)
		for pTech in self.sOrPrereqs:
			pTech.removeLeadsTo(self)
		for pTech in self.sLeadsTo:
			pTech.removePrereq(self)


	def __str__(self):
		str = self.getName()
		bFirst = True
		if (len(self.sAndPrereqs) > 0 or len(self.sOrPrereqs) > 0):
			str += " requires "
		if (len(self.sAndPrereqs) > 0):
			for pTech in self.sAndPrereqs:
				if bFirst:
					bFirst = False
				else:
					str += " and "
				str += pTech.getName()
		if (len(self.sOrPrereqs) > 0):
			if not bFirst:
				str += " and "
				bFirst = True
			for pTech in self.sOrPrereqs:
				if bFirst:
					bFirst = False
				else:
					str += " or "
				str += pTech.getName()
		if (len(self.sLeadsTo) > 0):
			str += ", leads to "
			bFirst = True
			for pTech in self.sLeadsTo:
				if bFirst:
					bFirst = False
				else:
					str += ", "
				str += pTech.getName()
		return str
