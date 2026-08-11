from Files import *

from Events import handler


# Constants

iNumModifiers = 14
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierColonyMaintenance,
iModifierCitiesMaintenance, iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, 
iModifierBuildingCost, iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)


# Modifiers

tDefaults = (100, 100, 100, 100, 100, 100, 100, 2, 100, 100, 100, 100, 100, 100)

MODIFIERS = CivFileMatrix("Modifiers.csv", tDefaults)

dLateScenarioModifiers = {
	iModifierUnitUpkeep : 90,
	iModifierDistanceMaintenance : 85,
	iModifierCitiesMaintenance : 80,
	iModifierCivicUpkeep : 90,
	iModifierInflationRate : 85,
	iModifierGreatPeopleThreshold : 85,
	iModifierGrowthThreshold : 80,
}


# Handlers

@handler("playerCivAssigned")
def init(iPlayer, iCivilization):
	updateModifiers(iPlayer, iCivilization)
	
	if scenario() > i3000BC and dBirth[iPlayer] < dBirth[iNorse]:
		adjustModifiers(iPlayer)
	
	player(iPlayer).updateMaintenance()


@handler("playerPeriodChange")
def onPeriodChange(iPlayer, iPeriod):
	if iPeriod == iPeriodMeiji:
		for iModifier in (iModifierResearchCost, iModifierCitiesMaintenance, iModifierCivicUpkeep, iModifierInflationRate):
			changeModifier(iPlayer, iModifier, -10)
	
	if iPeriod == iPeriodMing:
		for iModifier in (iModifierCitiesMaintenance, iModifierInflationRate):
			changeModifier(iPlayer, iModifier, -25)
		
		for iModifier in (iModifierCivicUpkeep, iModifierUnitCost, iModifierWonderCost):
			changeModifier(iPlayer, iModifier, -20)
		
		changeModifier(iPlayer, iModifierResearchCost, 10)


@handler("BeginGameTurn")
def updateLateModifiers(iGameTurn):			
	if scenario() == i3000BC and iGameTurn == year(600):
		for iPlayer in players.major().where(lambda p: dBirth[p] < dBirth[iNorse]):
			adjustInflationModifier(iPlayer)


# Implementation

def getModifier(iCivilization, iModifier):
	return MODIFIERS[iModifier, iCivilization]
	
def getAdjustedModifier(iPlayer, iModifier):
	if scenario() > i3000BC and dBirth[iPlayer] < dBirth[iNorse]:
		if iModifier in dLateScenarioModifiers:
			return getModifier(iPlayer, iModifier) * dLateScenarioModifiers[iModifier] / 100
	return getModifier(iPlayer, iModifier)
	
def setModifier(iPlayer, iModifier, iNewValue):
	player(iPlayer).setModifier(iModifier, iNewValue)
	
def changeModifier(iPlayer, iModifier, iChange):
	setModifier(iPlayer, iModifier, player(iPlayer).getModifier(iModifier) + iChange)
	
def adjustModifier(iPlayer, iModifier, iPercent):
	setModifier(iPlayer, iModifier, player(iPlayer).getModifier(iModifier) * iPercent / 100)
	
def adjustModifiers(iPlayer):
	for iModifier in dLateScenarioModifiers:
		adjustModifier(iPlayer, iModifier, dLateScenarioModifiers[iModifier])
		
def adjustInflationModifier(iPlayer):
	adjustModifier(iPlayer, iModifierInflationRate, dLateScenarioModifiers[iModifierInflationRate])
	
def updateModifier(iPlayer, iCivilization, iModifier):
	setModifier(iPlayer, iModifier, getModifier(iCivilization, iModifier))
	
def updateModifiers(iPlayer, iCivilization):
	for iModifier in range(iNumModifiers):
		updateModifier(iPlayer, iCivilization, iModifier)
