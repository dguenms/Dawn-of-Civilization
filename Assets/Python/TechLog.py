from Consts import *
from StoredData import sd
from RFCUtils import utils

def techlog(text):
	log("Techs.log", text.encode('ascii'))
	
def techstatus(text):
	log("TechStatus.log", text.encode('ascii'))

def onTechAcquired(iPlayer, iTech):
	if iPlayer >= iNumPlayers: return
	
	iYear = gc.getGame().getGameTurnYear()
	iColumn = gc.getTechInfo(iTech).getGridX()
	
	if iColumn > sd.getTechColumn(iPlayer):
		sd.setTechColumn(iPlayer, iColumn)
		techlog("Reached new column - year: %d, player: %s, column: %d" % (iYear, gc.getPlayer(iPlayer).getCivilizationShortDescription(0), iColumn))
		
def onFirstDiscovered(iPlayer, iTech):
	iYear = gc.getGame().getGameTurnYear()
	techlog("First to discover tech - year: %d, player: %s, tech: %s" % (iYear, gc.getPlayer(iPlayer).getCivilizationShortDescription(0), gc.getTechInfo(iTech).getText()))
	
def onReligionFounded(iPlayer, iReligion):
	if iPlayer >= iNumPlayers: return

	iYear = gc.getGame().getGameTurnYear()
	techlog("Founded religion - year: %d, player: %s, religion: %s" % (iYear, gc.getPlayer(iPlayer).getCivilizationShortDescription(0), gc.getReligionInfo(iReligion).getText()))
	
def checkTurn(iGameTurn):
	if iGameTurn % 10 == 1:
		iYear = gc.getGame().getGameTurnYear()
		techstatus("Tech Status - year: %d" % (iYear,))
		for iPlayer in range(iNumPlayers):
			logTechStatus(iPlayer)
		techstatus("")
		
def setup():
	iScenario = utils.getScenarioStartYear()
	iHandicap = gc.getGame().getHandicapType()
	iGamespeed = gc.getGame().getGameSpeedType()
	
	if iScenario >= 0:
		year = "%d AD" % iScenario
	else:
		year = "%d BC" % abs(iScenario)
	
	header = "LOG - %s Scenario - %s Difficulty - %s Speed" % (year, gc.getHandicapInfo(iHandicap).getText(), gc.getGameSpeedInfo(iGamespeed).getText())
	
	techlog(header)
	techlog("")
	
	techstatus(header)
	techstatus("")
		
def logTechStatus(iPlayer):
	if not gc.getPlayer(iPlayer).isAlive(): return
	
	lTechs = [gc.getTechInfo(iTech).getText() for iTech in range(iNumTechs) if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(iTech)]
	
	techstatus(" * player: %s, techs: %s" % (gc.getPlayer(iPlayer).getCivilizationShortDescription(0), str(lTechs)))