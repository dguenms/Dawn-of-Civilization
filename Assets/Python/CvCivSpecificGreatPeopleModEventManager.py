## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import CvEventManager
import CivSpecificGreatPeopleModNameUtils

gc = CyGlobalContext()

PyPlayer = PyHelpers.PyPlayer	

# globals
###################################################
class CvCivSpecificGreatPeopleModEventManager:

	def __init__(self, eventManager):
		# initialize base class

		eventManager.addEventHandler("greatPersonBorn", self.onGreatPersonBorn)
		# eventManager.addEventHandler("mouseEvent", self.onMouseEvent)

	

	"""
	# Test code to make sure that we can go through the vanilla great person
	# names and test the random names
	def onMouseEvent(self, argsList):
	
		gc.getPlayer(0).getCapitalCity().createGreatPeople(gc.getInfoTypeForString("UNIT_ARTIST"), true)
	"""
		
	def onGreatPersonBorn(self, argsList):
		'Great Person Born'
		pUnit, iPlayer, pCity = argsList
		player = PyPlayer(iPlayer)
		infoUnit = pUnit.getUnitClassType()
		
		# Check if we should even show the popup:
		if pUnit.isNone() or pCity.isNone():
			return
		
		if(len(pUnit.getNameNoDesc()) == 0): # Rename units with no names - important to avoid confusion with event log
			
			iCivilizationType = player.player.getCivilizationType()
			# Pass the civilization and unit type along to the renamer
			sName = CivSpecificGreatPeopleModNameUtils.generateCivilizationName(iCivilizationType, infoUnit)
			pUnit.setName(sName)
			if player.isHuman() or gc.getGame().getActiveTeam().canContact(iPlayer):
				CyInterface().addMessage(iHuman, True, con.iDuration, '%s (%s) has been born in %s.' %(sName, infoUnit, pCity.getName()), "Sounds\GreatPeople.wav", 0, "", ColorTypes(con.iYellow), pCity.getX(), pCity.getY(), True, True)
			else:
				CyInterface().addMessage(iHuman, True, con.iDuration, '%s (%s) has been born in a far away land.' %(sName, infoUnit), "Sounds\GreatPeople.wav", 0, "", ColorTypes(con.iYellow), -1, -1, True, True)
			

