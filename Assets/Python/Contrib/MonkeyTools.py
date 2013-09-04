## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
## 
## Author 	: 12 Monkeys - Tool Collection
## Date 	: 24.03.2006
## version 	: 1.2
## 

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import CvEventInterface

PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
localText = CyTranslator()

######################################################
### 	small debug function (stolen from Stone-D's ToolKit)
######################################################

def debug(argsList):
	printToScr = True
	printToLog = True
	message = "%s" %(argsList)
	if (printToScr):
		CyInterface().addImmediateMessage(message,"")
	if (printToLog):
		CvUtil.pyPrint(message)
	return 0
	
######################################################
### 	Class used for Re-Init Interceptor Mission 
######################################################

class ReInitInterceptorMision:

	def __init__(self):
		self.firsttime = true

	def doReInit(self):
		iPlayer = PyPlayer(CyGame().getActivePlayer())
		unitList = iPlayer.getUnitList()
		# Loop for all players cities
		for ii in range(len(unitList)):
			pLoopUnit = unitList[ii]
			# get the group the unit belongs to. 
			pGroup = pLoopUnit.getGroup()
			# check if unit is doing air patrol
			if (pGroup.getActivityType() == ActivityTypes.ACTIVITY_INTERCEPT):
				# remove mission (this one shold be obsolete, but who knows ;)
				pGroup.popMission()
				pPlot = pGroup.plot()
				# add new mission -> fortify
				pGroup.pushMission(MissionTypes.MISSION_FORTIFY, 0, 0, 0, false, false, MissionAITypes.NO_MISSIONAI, pPlot, pLoopUnit)
				# add new mission -> air patrol
				pGroup.pushMission(MissionTypes.MISSION_AIRPATROL, 0, 0, 0, false, false, MissionAITypes.NO_MISSIONAI, pPlot, pLoopUnit)

######################################################
### 	Calculates index of an XP point
######################################################

def GetIdxOfXP(iXP):
	iLevel = 0
	iIdx = 0
	while iLevel <= iXP:
		iIdx += 1
		if iIdx == 1:
			iLevel = 2
		else:
			iLevel += (iIdx-1)*2+1
	return iIdx-1

######################################################
### 	Calculates the number of possible promotions between two XP values
######################################################

def GetPossiblePromotions(iXP1, iXP2):
	iIdx1 = GetIdxOfXP(iXP1)
	iIdx2 = GetIdxOfXP(iXP2)
	return iIdx2-iIdx1+1
	
######################################################
### 	creates a list of possible upgrades for a unit
######################################################

def getPossibleUpgrades(pUnit):
	lList = []
	for i in range(gc.getNumUnitInfos()):
		if pUnit.canUpgrade(i, true):
			lList.append(i)
	return lList

######################################################
### 	creates a list of possible promotions for a unit
######################################################

def getPossiblePromos(pUnit):
	lList = []
	for i in range(gc.getNumPromotionInfos()):
		if pUnit.canAcquirePromotion(i):
			lList.append(i)
	return lList
	
######################################################
### 	checks if there are any possible upgrade for the unit
######################################################

def checkAnyUpgrade(pUnit):
	return (len(getPossibleUpgrades(pUnit)) > 0)

######################################################
### 	function returns a string which contains all the 
###		units characteristics the units get by promotions
######################################################
	
def getPromotionInfoText(pUnit):
	szPromotionInfo = u""
	bBlitz = false
	bAmphib = false
	bRiver = false
	bEnemyRoads = false
	bAlwaysHeal = false
	bHillsDoubleMove = false
	bImmuneToFirstStrikes = false
	lFeatureDoubleMove = [false]*gc.getNumFeatureInfos()
	iVisibilityChange = 0
	iMovesChange = 0
	iMoveDiscountChange = 0
	iWithdrawalChange = 0
	iCollateralDamageChange = 0
	iBombardRateChange = 0
	iFirstStrikesChange = 0
	iChanceFirstStrikesChange = 0
	iEnemyHealChange = 0
	iNeutralHealChange = 0
	iFriendlyHealChange = 0
	iSameTileHealChange = 0
	iAdjacentTileHealChange = 0
	iCombatPercent = 0
	iCityAttackPercent = 0
	iCityDefensePercent = 0
	iHillsDefensePercent = 0
	lFeatureDefensePercent = [0]*gc.getNumFeatureInfos()
	lUnitCombatModifierPercent = [0]*gc.getNumUnitCombatInfos()
	for i in range(gc.getNumPromotionInfos()):
		if pUnit.isHasPromotion(i):
			if gc.getPromotionInfo(i).isBlitz():
				bBlitz = true
			if gc.getPromotionInfo(i).isAmphib():
				bAmphib = true
			if gc.getPromotionInfo(i).isRiver():
				bRiver = true
			if gc.getPromotionInfo(i).isEnemyRoute():
				bEnemyRoads = true
			if gc.getPromotionInfo(i).isAlwaysHeal():
				bAlwaysHeal = true
			if gc.getPromotionInfo(i).isHillsDoubleMove():
				bHillsDoubleMove = true
			if gc.getPromotionInfo(i).isImmuneToFirstStrikes():
				bImmuneToFirstStrikes = true
			for ii in range(gc.getNumFeatureInfos()):
				if (gc.getPromotionInfo(i).getFeatureDoubleMove(ii)):
					lFeatureDoubleMove[ii] = true
			iTemp = gc.getPromotionInfo(i).getVisibilityChange()
			if iTemp > 0:
				iVisibilityChange += iTemp
			iTemp = gc.getPromotionInfo(i).getMovesChange()
			if iTemp > 0:
				iMovesChange += iTemp				
			iTemp = gc.getPromotionInfo(i).getMoveDiscountChange()
			if iTemp > 0:
				iMoveDiscountChange += iTemp
			iTemp = gc.getPromotionInfo(i).getWithdrawalChange()
			if iTemp > 0:
				iWithdrawalChange += iTemp
			iTemp = gc.getPromotionInfo(i).getCollateralDamageChange()
			if iTemp > 0:
				iCollateralDamageChange += iTemp
			iTemp = gc.getPromotionInfo(i).getBombardRateChange()
			if iTemp > 0:
				iBombardRateChange += iTemp
			iTemp = gc.getPromotionInfo(i).getFirstStrikesChange()
			if iTemp > 0:
				iFirstStrikesChange += iTemp
			iTemp = gc.getPromotionInfo(i).getChanceFirstStrikesChange()
			if iTemp > 0:
				iChanceFirstStrikesChange += iTemp
			iTemp = gc.getPromotionInfo(i).getEnemyHealChange()
			if iTemp > 0:
				iEnemyHealChange += iTemp
			iTemp = gc.getPromotionInfo(i).getNeutralHealChange()
			if iTemp > 0:
				iNeutralHealChange += iTemp
			iTemp = gc.getPromotionInfo(i).getFriendlyHealChange()
			if iTemp > 0:
				iFriendlyHealChange += iTemp
			iTemp = gc.getPromotionInfo(i).getSameTileHealChange()
			if iTemp > 0:
				iSameTileHealChange += iTemp
			iTemp = gc.getPromotionInfo(i).getAdjacentTileHealChange()
			if iTemp > 0:
				iAdjacentTileHealChange += iTemp
			iTemp = gc.getPromotionInfo(i).getCombatPercent()
			if iTemp > 0:
				iCombatPercent += iTemp
			iTemp = gc.getPromotionInfo(i).getCityAttackPercent()
			if iTemp > 0:
				iCityAttackPercent += iTemp
			iTemp = gc.getPromotionInfo(i).getCityDefensePercent()
			if iTemp > 0:
				iCityDefensePercent += iTemp
			iTemp = gc.getPromotionInfo(i).getHillsDefensePercent()
			if iTemp > 0:
				iHillsDefensePercent += iTemp
			for ii in range(gc.getNumFeatureInfos()):
				iTemp = gc.getPromotionInfo(i).getFeatureDefensePercent(ii)
				if (iTemp > 0):
					lFeatureDefensePercent[ii] += iTemp
			for ii in range(gc.getNumUnitCombatInfos()):
				if gc.getPromotionInfo(i).getUnitCombat(ii):
					iTemp = gc.getPromotionInfo(i).getUnitCombatModifierPercent(ii)
					if iTemp > 0:
						lUnitCombatModifierPercent[ii] += iTemp
				
	if bBlitz:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_BLITZ_TEXT", ()) + "\n"
	if bAmphib:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_AMPHIB_TEXT", ()) + "\n"
	if bRiver:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_RIVER_ATTACK_TEXT", ()) + "\n"
	if bEnemyRoads:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_ENEMY_ROADS_TEXT", ()) + "\n"
	if bAlwaysHeal:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_ALWAYS_HEAL_TEXT", ()) + "\n"
	if bHillsDoubleMove:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_HILLS_MOVE_TEXT", ()) + "\n"
	if bImmuneToFirstStrikes:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_IMMUNE_FIRST_STRIKES_TEXT", ()) + "\n"
	szTemp = u""
	for ii in range(gc.getNumFeatureInfos()):
		if lFeatureDoubleMove[ii]:
			if len(szTemp) > 0:
				szTemp += u", "
			szTemp += gc.getFeatureInfo(ii).getDescription()
	if len(szTemp) > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_DOUBLE_MOVE_TEXT", (szTemp, )) + "\n"
	if iVisibilityChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_VISIBILITY_TEXT", (iVisibilityChange, )) + "\n"
	if iMovesChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_MOVE_TEXT", (iMovesChange, )) + "\n"
	if iMoveDiscountChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_MOVE_DISCOUNT_TEXT", (iMoveDiscountChange, )) + "\n"
	if iWithdrawalChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_WITHDRAWAL_TEXT", (iWithdrawalChange, )) + "\n"
	if iCollateralDamageChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_COLLATERAL_DAMAGE_TEXT", (iCollateralDamageChange, )) + "\n"
	if iBombardRateChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_BOMBARD_TEXT", (iBombardRateChange, )) + "\n"
	if iFirstStrikesChange == 1:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_FIRST_STRIKE_TEXT", (iFirstStrikesChange, )) + "\n"
	if iFirstStrikesChange > 1:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_FIRST_STRIKES_TEXT", (iFirstStrikesChange, )) + "\n"
	if iChanceFirstStrikesChange == 1:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_FIRST_STRIKE_CHANCE_TEXT", (iChanceFirstStrikesChange, )) + "\n"
	if iChanceFirstStrikesChange > 1:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_FIRST_STRIKES_CHANCE_TEXT", (iChanceFirstStrikesChange, )) + "\n"
	if iEnemyHealChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT", (iEnemyHealChange, )) + localText.getText("TXT_KEY_PROMOTION_ENEMY_LANDS_TEXT", ()) + "\n"
	if iNeutralHealChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT", (iNeutralHealChange, )) + localText.getText("TXT_KEY_PROMOTION_NEUTRAL_LANDS_TEXT", ()) + "\n"
	if iFriendlyHealChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_HEALS_EXTRA_TEXT", (iFriendlyHealChange, )) + localText.getText("TXT_KEY_PROMOTION_FRIENDLY_LANDS_TEXT", ()) + "\n"
	if iSameTileHealChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_HEALS_SAME_TEXT", (iSameTileHealChange, )) + localText.getText("TXT_KEY_PROMOTION_DAMAGE_TURN_TEXT", ()) + "\n"
	if iAdjacentTileHealChange > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_HEALS_ADJACENT_TEXT", (iAdjacentTileHealChange, )) + localText.getText("TXT_KEY_PROMOTION_DAMAGE_TURN_TEXT", ()) + "\n"
	if iCombatPercent > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_STRENGTH_TEXT", (iCombatPercent, )) + "\n"
	if iCityAttackPercent > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_CITY_ATTACK_TEXT", (iCityAttackPercent, )) + "\n"
	if iCityDefensePercent > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_CITY_DEFENSE_TEXT", (iCityDefensePercent, )) + "\n"
	if iHillsDefensePercent > 0:
		szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_HILLS_DEFENSE_TEXT", (iHillsDefensePercent, )) + "\n"
	szTemp = u""
	for ii in range(gc.getNumFeatureInfos()):
		iTemp = lFeatureDefensePercent[ii]
		if iTemp > 0:
			szTemp = gc.getFeatureInfo(ii).getDescription()
			szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_DEFENSE_TEXT", (iTemp, szTemp, )) + "\n"
	szTemp = u""
	for ii in range(gc.getNumUnitCombatInfos()):
		iTemp = lUnitCombatModifierPercent[ii]
		if iTemp > 0:
			szTemp = gc.getUnitCombatInfo(ii).getDescription()
			szPromotionInfo += localText.getText("TXT_KEY_PROMOTION_VERSUS_TEXT", (iTemp, szTemp, )) + "\n"		
	return u"<font=2>" + szPromotionInfo + u"</font>"
	
######################################################
### 	removes the pedia links from a string
######################################################	

def removeLinks(szText):
	# replace link starts
	while szText.find("<link=") != -1:
		iStartPos = szText.find("<link=")
		iEndPos = szText.find(">", iStartPos)
		szText = szText[:iStartPos]+szText[iEndPos+1:]			
	# replace link ends
	szText = szText.replace("</link>", "")		
	return szText

######################################################
### 	removes the font literals from a texts
######################################################

def removeFonts(szText):
	# replace link starts
	while szText.find("<font=") != -1:
		iStartPos = szText.find("<font=")
		iEndPos = szText.find(">", iStartPos)
		szText = szText[:iStartPos]+szText[iEndPos+1:]			
	# replace link ends
	szText = szText.replace("</font>", "")		
	return szText
	
######################################################
### 	removes the color literals from a texts
######################################################

def removeColor(szText):
	# replace link starts
	while szText.find("<color=") != -1:
		iStartPos = szText.find("<color=")
		iEndPos = szText.find(">", iStartPos)
		szText = szText[:iStartPos]+szText[iEndPos+1:]			
	# replace link ends
	szText = szText.replace("</color>", "")		
	return szText
	
######################################################
### 	calculates the heal factor per round for a unit. 
###		Takes consideration of city-buildings and 
###		units incl. their promotions on the actual and 
###		adjacent plots. Does only work for player units.
######################################################

def getPlotHealFactor(pUnit):

	# heal rates for certain areas. They are usually stored in the GlobalDefines.XML but can't be read out with a standard API function.
	# So I placed them here as constants.
	ENEMY_HEAL_RATE				= 5
	NEUTRAL_HEAL_RATE			= 10
	FRIENDLY_HEAL_RATE			= 15
	CITY_HEAL_RATE				= 20

	
	# set/reset some variables
	pPlot = pUnit.plot()
	iSameTileHealFactor 		= 0
	iAdjacentTileHealFactor 	= 0
	iBuildingHealFactor 		= 0
	iSelfHealFactor 			= 0
	iPromotionHealFactor 		= 0
	iTileHealFactor 			= 0
	iActivePlayer 				= CyGame().getActivePlayer()
	pActivePlayer 				= gc.getPlayer(iActivePlayer)
	iActivePlayerTeam 			= pActivePlayer.getTeam()
	eDomain 					= gc.getUnitInfo(pUnit.getUnitType()).getDomainType()
	
	# a sea or air unit in a city, behaves like a land unit
	if pPlot.isCity():
		eDomain = DomainTypes.DOMAIN_LAND

	# calculate the adjacent-tile heal-factor caused by other units (only the unit with the highest factor counts)
	for dx in range(-1, 2):
		for dy in range(-1, 2):
			# ignore same tile. Adjacent-tile healing does not work on the same tile.
			if not (dx == 0 and dy == 0):
				pLoopPlot = CyMap().plot(pPlot.getX()+dx, pPlot.getY()+dy)
				# loop through all units on the plot
				for i in range(pLoopPlot.getNumUnits()):
					pLoopUnit = pLoopPlot.getUnit(i)
					eLoopUnitDomain = gc.getUnitInfo(pLoopUnit.getUnitType()).getDomainType()
					# a sea or air unit in a city, behaves like a land unit
					if pLoopPlot.isCity():
						eLoopUnitDomain = DomainTypes.DOMAIN_LAND
					# adjacent-tile heal does only work if the units have the same domain type
					if (eDomain == eLoopUnitDomain):
						if (pLoopUnit.getTeam() == iActivePlayerTeam):
							if (pLoopUnit.getAdjacentTileHeal() > iAdjacentTileHealFactor):
								iAdjacentTileHealFactor = pLoopUnit.getAdjacentTileHeal()
	
	# calculate the same-tile heal-factor caused by other or same unit (only the unit with the highest factor counts)
	# the same-tile healing is also a kind of self-healing. Means : the promotion Medic I has also effect on the owner unit
	for i in range(pPlot.getNumUnits()):
		pLoopUnit = pPlot.getUnit(i)
		eLoopUnitDomain = gc.getUnitInfo(pLoopUnit.getUnitType()).getDomainType()
		# a sea or air unit in a city, behaves like a land unit
		if pLoopPlot.isCity():
			eLoopUnitDomain = DomainTypes.DOMAIN_LAND
		# same tile heal does only work if the units are of the same domain type
		if (eDomain == eLoopUnitDomain):
			if (pLoopUnit.getTeam() == iActivePlayerTeam):
				if (pLoopUnit.getSameTileHeal() > iSameTileHealFactor):
					iSameTileHealFactor = pLoopUnit.getSameTileHeal()
				
	# only the highest value counts
	iTileHealFactor = max(iAdjacentTileHealFactor, iSameTileHealFactor)

	# calculate the self heal factor by the location and promotion
	iTeam = pPlot.getTeam()
	pTeam = gc.getTeam(iTeam)		
	iSelfHealFactor 		= NEUTRAL_HEAL_RATE
	iPromotionHealFactor 	= pUnit.getExtraNeutralHeal()
	if pPlot.isCity():
		iSelfHealFactor 		= CITY_HEAL_RATE
		iPromotionHealFactor 	= pUnit.getExtraFriendlyHeal()
	elif (iTeam == iActivePlayerTeam):
		iSelfHealFactor 		= FRIENDLY_HEAL_RATE
		iPromotionHealFactor 	= pUnit.getExtraFriendlyHeal()
	elif (iTeam != TeamTypes.NO_TEAM):
		if (pTeam.isAtWar(iActivePlayerTeam)):
			iSelfHealFactor 		= ENEMY_HEAL_RATE
			iPromotionHealFactor 	= pUnit.getExtraEnemyHeal()
	
	# calculate the heal factor by city buildings
	if pPlot.isCity():
		if (pPlot.getTeam() == iActivePlayerTeam):
			# EF: should probably allow friendly healing too, but this doesn't
			pCity = pPlot.getPlotCity()
			# loop for all buldings
			for iBuilding in range(gc.getNumBuildingInfos()):
				# check if city has that building
				if pCity.getNumActiveBuilding(iBuilding) > 0:
					# sum up all heal rates 
					iBuildingHealFactor += gc.getBuildingInfo(iBuilding).getHealRateChange() * pCity.getNumActiveBuilding(iBuilding)

	# return the sum of all heal factors
	return iTileHealFactor + iBuildingHealFactor + iSelfHealFactor + iPromotionHealFactor	

######################################################
### 	calculates the upgrade price for a unit 
###		nMode is :
###			0 : only the actual unit
###			1 : all units of the same type in the same selection group
###			2 : all units of the same type on the same plot
###			3 : all player units of the same type all over the map
######################################################
		
def getUpgradePrice(pUnit, iToUnitType, nMode):
	# single unit
	if nMode == 0:
		return pUnit.upgradePrice(iToUnitType)
	# selection group
	elif nMode == 1:
		pPlot = pUnit.plot()
		iPrice = 0
		for i in range(pPlot.getNumUnits()):
			pLoopUnit = pPlot.getUnit(i)
			if (pLoopUnit.getGroupID() == pUnit.getGroupID()) and (pLoopUnit.getUnitType() == pUnit.getUnitType()):
				iPrice += pLoopUnit.upgradePrice(iToUnitType)
		return iPrice
	# same plot
	elif nMode == 2:
		pPlot = pUnit.plot()
		iPrice = 0
		for i in range(pPlot.getNumUnits()):
			pLoopUnit = pPlot.getUnit(i)
			if (pLoopUnit.getUnitType() == pUnit.getUnitType()):
				iPrice += pLoopUnit.upgradePrice(iToUnitType)
		return iPrice
	# all players unit
	elif nMode == 3:
		pActPlayer = gc.getActivePlayer()
		iPrice = 0
		for i in range(pActPlayer.getNumUnits()):
			pLoopUnit = pActPlayer.getUnit(i)
			if (pLoopUnit.getUnitType() == pUnit.getUnitType()):
				iPrice += pLoopUnit.upgradePrice(iToUnitType)
		return iPrice
	return -1

######################################################
### 	some keyboard hooks
######################################################

def bShift():
	return CvEventInterface.getEventManager().bShift

def bCtrl():
	return CvEventInterface.getEventManager().bCtrl

def bAlt():
	return CvEventInterface.getEventManager().bAlt
		
######################################################
### 	END 
######################################################
