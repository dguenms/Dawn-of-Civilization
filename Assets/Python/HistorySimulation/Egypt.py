from Events import handler
from PyHelpers import *
from RFCUtils import *
from AIWars import spawnConquerors
from Secession import secedeCity
from HistoryModUtils import *
from Locations import tThebes, tInebuHedj, tBwhen, tMedewi

pEgypt = None
cInebuHedj = None
cThebes = None
dHyksosConquestUnits = {
    iHarass: 3,
    iCityAttack: 1,
    iDefend: 1,
}
dNubianConquestUnits = {
    iHarass: 3,
    iCityAttack: 2,
    iDefend: 1
}

@handler("GameStart")
def initializeEgypt():
    global pEgypt, cInebuHedj, cThebes
    pEgypt = PyPlayer(player(iEgypt).getID())
    cInebuHedj = city(tInebuHedj)
    cThebes = city(tThebes)

    # Force research of Masonry at the start of the game
    pEgypt.pushResearch(iMasonry, True)

@handler("OnLoad")
def reloadGlobalVariables():
    global pEgypt, cInebuHedj, cThebes
    pEgypt = PyPlayer(player(iEgypt).getID())
    cInebuHedj = city(tInebuHedj)
    cThebes = city(tThebes)

@handler("BeginPlayerTurn")
def EgyptHistory(iGameTurn, iPlayer):
    if civ(iPlayer) == iEgypt:

        # 2850BC: Force completion of Masonry, switch to slavery (with no anarchy), 
        # begin quarry construction next to Inebu-Hedj, start researching Sailing
        if iGameTurn == year(-2850):
            completeResearch(pEgypt, iMasonry)
            pEgypt.setCivic(iCivicsSociety, iSlavery)
            uWorker = pEgypt.getUnitsOfType(iWorker)[0]                    
            unit_MoveAndMission(uWorker, 78, 43, MissionTypes.MISSION_BUILD, MissionAITypes.NO_MISSIONAI, iQuarry)
            pushResearch(pEgypt, iSailing)

        # 2780BC: Force completion of the quarry and Begin construction of the Pyramids in Inebu-Hedj
        if iGameTurn == year(-2780):
            setImprovement(78, 43, iQuarry)
            pushBuildingProduction(cInebuHedj, iPyramids)

        # 2686 BC: Move capital to Inebu-Hedj and complete research of Sailing, then start researching Tanning
        if iGameTurn == year(-2686):
            relocateCapital(iEgypt, tInebuHedj)
            completeResearch(pEgypt, iSailing)
            pushResearch(pEgypt, iTanning)

        # 2600 BC: Complete the pyramids
        if iGameTurn == year(-2600):
            completeBuildingProduction(cInebuHedj, iPyramids)

        # 2580 BC: Start working on the Great Sphinx
        if iGameTurn == year(-2580):
            pushBuildingProduction(cInebuHedj, iGreatSphinx)

        # 2540 BC: Complete the Great Sphinx, complete Tanning, 
        # start researching Seafaring and start working on a Pesedjet Temple 
        if iGameTurn == year(-2540):
            completeBuildingProduction(cInebuHedj, iGreatSphinx)
            completeResearch(pEgypt, iTanning)
            pushResearch(pEgypt, iSeafaring)
        
        if iGameTurn == year(-2520):
            pushBuildingProduction(cInebuHedj, unique_building(iEgypt, iPaganTemple))

        # 2350 BC: Complete the research of Seafaring, beeline for construction
        if iGameTurn == year(-2350):
            completeResearch(pEgypt, iSeafaring)
            pushResearch(pEgypt, iConstruction)

        # 2250 BC: 2 turns of unrest in Inebu-Hedj, complete one tech if it's not construction
        if iGameTurn == year(-2250):
            cInebuHedj.setOccupationTimer(2)
            if pEgypt.getCurrentTech() != iConstruction:
                completeResearch(pEgypt, pEgypt.getCurrentTech())
            
        # 2200 BC: Destroy the farm improvements
        if iGameTurn == year(-2200):
            setImprovement(80, 40, -1)
            setImprovement(79, 44, -1)
            setImprovement(79, 39, -1)
            setImprovement(79, 42, -1)

        # 2184 BC: First intermediate period: Inebu-Hedj becomes independent, unrest in both cities during the period and
        # population and culture decay
        if iGameTurn == year(-2184):
            secedeCity(cInebuHedj, slot(iIndependent), False, 20, 0, 3)
            team(iEgypt).declareWar(team(iIndependent).getID(), True, -1)
            cThebes.setOccupationTimer(4)
            cThebes.changePopulation(-2)
            cThebes.setCulture(pEgypt.getID(), 10, True)

        # 2150 BC: Complete another tech if it's not construction
        if iGameTurn == year(-2150):
            if pEgypt.getCurrentTech() != iConstruction:
                completeResearch(pEgypt, pEgypt.getCurrentTech())
                
        # 2040 BC: End of the first intermediate period, Mentuhotep II reconquers the North, complete a tech if it's not construction
        if iGameTurn == year(-2040):
            spawnConquerors(iEgypt, iIndependent, tInebuHedj, tInebuHedj, 1, -2040, 0, WarPlanTypes.WARPLAN_DOGPILE, 0)
            # From onCityAcquired_Egypt, Inebu-Hedj will produce a Settler immediately after reconquering and a worker
            # will be made in the city if there are none
            if pEgypt.getCurrentTech() != iConstruction:
                completeResearch(pEgypt, pEgypt.getCurrentTech())

        # 1991 BC: Switch 40% of melee units to archers
        if iGameTurn == year(-1991):
            uMelee = pEgypt.getUnitsOfType(iMilitia) + pEgypt.getUnitsOfType(iSpearman)
            iCount = int(len(uMelee) * 0.4)
            for i in range(iCount):
                replace(uMelee[i], iArcher)

        # 1971 BC: Capital is moved back to Inebu-Hedj
        if iGameTurn == year(-1971):
            relocateCapital(iEgypt, tInebuHedj)

        # 1950 BC: Complete the research of Construction
        if iGameTurn == year(-1950):
            completeResearch(pEgypt, iConstruction)            
        
        # 1925 BC: Start working on the farm on (78, 42) and complete the Settler in Inebu-Hedj, send it 
        # towards Nubia with an archer to found Bwhen (settler handled in onUnitBuilt_Egypt)
        # If AI: City will be directly founded later
        if iGameTurn == year(-1925):
            uWorker = pEgypt.getUnitsOfType(iWorker)[0]
            unit_MoveAndMission(uWorker, 78, 42, MissionTypes.MISSION_BUILD, MissionAITypes.NO_MISSIONAI, iFarm)
            if player(iEgypt).isHuman():
                completeUnitProduction(cInebuHedj, iSettler)
                uArcher = None
                for unit in units.at(tInebuHedj).type(iArcher):
                    uArcher = unit
                    break
                if uArcher == None:
                    uArcher = makeUnit(iEgypt, iArcher, tInebuHedj, UnitAITypes.UNITAI_CITY_DEFENSE)
                unit_MoveAndMission(uArcher, 79, 41, MissionTypes.MISSION_FORTIFY, MissionAITypes.MISSIONAI_GUARD_CITY)
        
        # 1875 BC: Complete the farm on (78, 42), send the worker to build a mine on (81,43)
        if iGameTurn == year(-1875):
            setImprovement(78, 42, iFarm)
            uWorker = pEgypt.getUnitsOfType(iWorker)[0]
            unit_MoveAndMission(uWorker, 81, 43, MissionTypes.MISSION_BUILD, MissionAITypes.NO_MISSIONAI, iMine)

        # 1850 BC: Bwhen is founded with walls, and the archer is sent to fortify now that the tile is accessible, handled in onCityBuilt_Egypt
        if iGameTurn == year(-1850):
            if not player(iEgypt).isHuman():
                player(iEgypt).found(78, 40)
                uArcher = pEgypt.getUnitsOfType(iArcher)[0]
                unit_MoveAndMission(uArcher, 78, 40, MissionTypes.MISSION_FORTIFY, MissionAITypes.MISSIONAI_GUARD_CITY)

        # 1825 BC: Complete the mine on (81, 43)
        if iGameTurn == year(-1825):
            setImprovement(81, 43, iMine)

        # 1790 BC: Second intermediate period begins, Inebu-Hedj becomes independent, Thebes loses culture and population
        if iGameTurn == year(-1790):
            secedeCity(cInebuHedj, slot(iIndependent), False, 20, 0)
            cThebes.changePopulation(-2)
            cThebes.setCulture(pEgypt.getID(), 10, True)
            if pEgypt.getUnitsOfType(iArcher) == []: # Make sure there are defenders in Thebes
                makeUnit(iEgypt, iArcher, tThebes, UnitAITypes.UNITAI_CITY_DEFENSE)


        # 1750 BC: Destruction of a farm, Bwhen is abandoned and razed by Nubians, handled in Minors.py
        if iGameTurn == year(-1750):
            setImprovement(78, 42, -1)
            for unit in units.at(tBwhen):
                unit.kill(False, -1)

        # 1700 BC: Destruction of more farms
        if iGameTurn == year(-1700):
            setImprovement(79, 44, -1)
            setImprovement(80, 40, -1)
            
        # 1650 BC: The Hyksos invade Egypt, and conquer the independent city of Inebu-Hedj, handled in Minors.py
        # Egypt learns to make Chariots from them, send a worker to build a pasture on the horse (80, 42) with 
        # a spearman as escort, make the units if there are none
        if iGameTurn == year(-1650):
            if plot(80, 42).getImprovementType() != iPasture:
                uWorker = pEgypt.getUnitsOfType(iWorker)
                uSpearman = pEgypt.getUnitsOfType(iSpearman)
                if uWorker == []:
                    uWorker = makeUnit(iEgypt, iWorker, tThebes, UnitAITypes.UNITAI_WORKER)
                else:
                    uWorker = uWorker[0]
                if uSpearman == []:
                    uSpearman = makeUnit(iEgypt, iSpearman, tThebes, UnitAITypes.UNITAI_CITY_DEFENSE)
                else:
                    uSpearman = uSpearman[0]
                unit_MoveAndMission(uWorker, 80, 42, MissionTypes.MISSION_BUILD, MissionAITypes.NO_MISSIONAI, iPasture)
                unit_MoveAndMission(uSpearman, 80, 42, MissionTypes.MISSION_FORTIFY, MissionAITypes.MISSIONAI_GUARD_BONUS)

        # 1600 BC: Pasture is completed, leader changes to Hatshepsut (handled in DynamicCivs.py)
        if iGameTurn == year(-1600):
            if plot(80, 42).getImprovementType() != iPasture:
                setImprovement(80, 42, iPasture)

        # 1580 BC: One turn of unrest in Thebes
        if iGameTurn == year(-1580):
            cThebes.setOccupationTimer(1)
        
        # 1550 BC: The Hyksos are defeated, civ name becomes New Kingdom of Egypt (handled in DynamicCivs.py), units spawn one turn early
        if iGameTurn == year(-1575):
            spawnConquerors(iEgypt, iBarbarian, tInebuHedj, tInebuHedj, 1, -1550, 0, WarPlanTypes.WARPLAN_DOGPILE, 0, dHyksosConquestUnits)

        # 1540 BC: Nubia is settled one again on (78, 39) in 1520BC the city of Para with an archer and a war chariot
        # Conqueror event against the Nubian capital Medewi
        if iGameTurn == year(-1540):
            if player(iEgypt).isHuman():            
                makeUnit(iEgypt, iSettler, (78, 39), UnitAITypes.UNITAI_SETTLE)
            makeUnit(iEgypt, iArcher, (78, 39), UnitAITypes.UNITAI_CITY_DEFENSE)
            uWarChariot = find_min(pEgypt.getUnitsOfType(iWarChariot), lambda u: distance((78, 39), (u.getX(), u.getY()))).result
            unit_MoveAndMission(uWarChariot, 78, 39, MissionTypes.MISSION_FORTIFY, MissionAITypes.MISSIONAI_GUARD_CITY)
            spawnConquerors(iEgypt, slot(iNubia), tMedewi, tMedewi, 1, -1520, 0, WarPlanTypes.WARPLAN_DOGPILE, 0, dNubianConquestUnits)
            plot(tMedewi).resetBirthProtected()


        # 1520 BC: Para foundation for AI
        if iGameTurn == year(-1520):
            if not player(iEgypt).isHuman():
                player(iEgypt).found(78, 39)
                

@handler("cityAcquiredAndKept")
def onCityAcquired_Egypt(iPlayer, iCity):
    global cInebuHedj
    iCiv = civ(iPlayer)
    if iCiv == iEgypt:
        cCity = city(iCity)

        # 2040BC: Produce a settler immediately after reconquering Inebu-Hedj
        # Make a worker unit if there are none
        if player(iEgypt).getPeriod() == iPeriodMiddleKingdom or player(iEgypt).getPeriod() == iPeriodOldKingdom:
            cInebuHedj = cCity
            pushUnitProduction(cCity, iSettler)
            if pEgypt.getUnitsOfType(iWorker) == []:
                if cThebes.getProductionUnit() == iWorker:
                    completeUnitProduction(cThebes, iWorker)
                else:
                    makeUnit(iEgypt, iWorker, tInebuHedj, UnitAITypes.UNITAI_WORKER)


@handler("unitBuilt")
def onUnitBuilt_Egypt(iCity, uUnit):
    cCity = city(iCity)

    # 1925BC: Send the settler towards Nubia with an archer to found Bwhen
    if cCity.getOwner() == pEgypt.getID():
        if uUnit.getUnitType() == iSettler:
            unit_MoveAndMission(uUnit, 78, 40, MissionTypes.MISSION_FOUND, MissionAITypes.MISSIONAI_FOUND) # Bwhen


@handler("cityBuilt")
def onCityBuilt_Egypt(iCity):
    cCity = city(iCity)

    # 1850 BC: Bwhen is founded and starts with walls, if not AI send the archer to fortify now that the tile is accessible 
    if cCity.getName() == "Bwhen":
        if player(iEgypt).isHuman():
            for unit in units.at((79, 41)).type(iArcher):
                unit_MoveAndMission(unit, 78, 40, MissionTypes.MISSION_FORTIFY, MissionAITypes.MISSIONAI_GUARD_CITY)
        cCity.setHasRealBuilding(iWalls, True)