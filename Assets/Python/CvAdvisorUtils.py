## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
## 
## CvAdvisorUtils


from CvPythonExtensions import *
import PyHelpers


gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer


g_iAdvisorNags = 0
g_listNoLiberateCities = []


def resetAdvisorNags():
	global g_iAdvisorNags
	g_iAdvisorNags = 0
	
def resetNoLiberateCities():
	global g_listNoLiberateCities
	g_listNoLiberateCities = []
	
def featPopup(iPlayer):
	if (not gc.getPlayer(iPlayer).isOption(PlayerOptionTypes.PLAYEROPTION_ADVISOR_POPUPS)):
		return False
	if (not gc.getPlayer(iPlayer).isHuman()):
		return False
	if (gc.getGame().isNetworkMultiPlayer()):
		return False
	if (gc.getGame().getElapsedGameTurns() == 0):
		return False
	return True


def populationFeat(iPlayer, eFeat, szText):

	if (not gc.getPlayer(iPlayer).isFeatAccomplished(eFeat)):
	
		gc.getPlayer(iPlayer).setFeatAccomplished(eFeat, True)
		
		if (featPopup(iPlayer)):
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setData1(eFeat)
			popupInfo.setText(localText.getText(szText, (gc.getPlayer(iPlayer).getCivilizationDescriptionKey(), )))
			popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
			popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
			popupInfo.addPopup(iPlayer)

def unitBuiltFeats(pCity, pUnit):
	
	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_ARCHER)):

		if (pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ARCHER")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_ARCHER, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNITCOMBAT_ARCHER)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNITCOMBAT_ARCHER", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())
	
	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_MOUNTED)):

		if (pUnit.getUnitCombatType() in [gc.getInfoTypeForString("UNITCOMBAT_LIGHT_CAVALRY"), gc.getInfoTypeForString("UNITCOMBAT_HEAVY_CAVALRY")]):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_MOUNTED, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNITCOMBAT_MOUNTED)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNITCOMBAT_MOUNTED", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())
		
	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_MELEE)):

		if (pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_MELEE")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_MELEE, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNITCOMBAT_MELEE)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNITCOMBAT_MELEE", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())

	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_SIEGE)):

		if (pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_SIEGE")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_SIEGE, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNITCOMBAT_SIEGE)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNITCOMBAT_SIEGE", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())
	
	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_GUN)):

		if (pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_GUN")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_GUN, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNITCOMBAT_GUN)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNITCOMBAT_GUN", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())
	
	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_ARMOR)):

		if (pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_ARMOR")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_ARMOR, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNITCOMBAT_ARMOR)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNITCOMBAT_ARMOR", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())
	
	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_HELICOPTER)):

		if (pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_HELICOPTER")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_HELICOPTER, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNITCOMBAT_HELICOPTER)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNITCOMBAT_HELICOPTER", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())
	
	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_NAVAL)):

		if (pUnit.getUnitCombatType() == gc.getInfoTypeForString("UNITCOMBAT_NAVAL")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNITCOMBAT_NAVAL, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNITCOMBAT_NAVAL)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNITCOMBAT_NAVAL", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())

	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNIT_PRIVATEER)):

		if (pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_PRIVATEER")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNIT_PRIVATEER, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNIT_PRIVATEER)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNIT_PRIVATEER", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())

	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_UNIT_SPY)):

		if (pUnit.getUnitType() == gc.getInfoTypeForString("UNIT_SPY")):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_UNIT_SPY, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_UNIT_SPY)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_UNIT_SPY", (pUnit.getNameKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())

def buildingBuiltFeats(pCity, iBuildingType):
	
	if (not gc.getPlayer(pCity.getOwner()).isFeatAccomplished(FeatTypes.FEAT_NATIONAL_WONDER)):

		if (isNationalWonderClass(gc.getBuildingInfo(iBuildingType).getBuildingClassType())):
		
			gc.getPlayer(pCity.getOwner()).setFeatAccomplished(FeatTypes.FEAT_NATIONAL_WONDER, True)
			
			if (featPopup(pCity.getOwner()) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setData1(FeatTypes.FEAT_NATIONAL_WONDER)
				popupInfo.setData2(pCity.getID())
				popupInfo.setText(localText.getText("TXT_KEY_FEAT_NATIONAL_WONDER", (gc.getBuildingInfo(iBuildingType).getTextKey(), pCity.getNameKey(), )))
				popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
				popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
				popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
				popupInfo.addPopup(pCity.getOwner())

def endTurnFeats(iPlayer):

	lRealPopulation = gc.getPlayer(iPlayer).getRealPopulation()

	if (lRealPopulation > 500000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_HALF_MILLION, "TXT_KEY_FEAT_HALF_MILLION")
	if (lRealPopulation > 1000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_1_MILLION, "TXT_KEY_FEAT_1_MILLION")
	if (lRealPopulation > 2000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_2_MILLION, "TXT_KEY_FEAT_2_MILLION")
	if (lRealPopulation > 5000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_5_MILLION, "TXT_KEY_FEAT_5_MILLION")
	if (lRealPopulation > 10000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_10_MILLION, "TXT_KEY_FEAT_10_MILLION")
	if (lRealPopulation > 20000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_20_MILLION, "TXT_KEY_FEAT_20_MILLION")
	if (lRealPopulation > 50000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_50_MILLION, "TXT_KEY_FEAT_50_MILLION")
	if (lRealPopulation > 100000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_100_MILLION, "TXT_KEY_FEAT_100_MILLION")
	if (lRealPopulation > 200000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_200_MILLION, "TXT_KEY_FEAT_200_MILLION")
	if (lRealPopulation > 500000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_500_MILLION, "TXT_KEY_FEAT_500_MILLION")
	if (lRealPopulation > 1000000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_1_BILLION, "TXT_KEY_FEAT_1_BILLION")
	if (lRealPopulation > 2000000000):
		populationFeat(iPlayer, FeatTypes.FEAT_POPULATION_2_BILLION, "TXT_KEY_FEAT_2_BILLION")

	if (not gc.getPlayer(iPlayer).isFeatAccomplished(FeatTypes.FEAT_TRADE_ROUTE)):
	
		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			if (not pCity.isCapital()):
				if (pCity.isConnectedToCapital(iPlayer)):
					gc.getPlayer(iPlayer).setFeatAccomplished(FeatTypes.FEAT_TRADE_ROUTE, True)
					
					if (featPopup(iPlayer) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setData1(FeatTypes.FEAT_TRADE_ROUTE)
						popupInfo.setData2(pCity.getID())
						popupInfo.setText(localText.getText("TXT_KEY_FEAT_TRADE_ROUTE", (pCity.getNameKey(), )))
						popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
						popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
						popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
						popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
						popupInfo.addPopup(iPlayer)
					
					break

	pCapitalCity = gc.getPlayer(iPlayer).getCapitalCity()

	if (not pCapitalCity.isNone()):

		if (not gc.getPlayer(iPlayer).isFeatAccomplished(FeatTypes.FEAT_COPPER_CONNECTED)):
		
			iBonus = gc.getInfoTypeForString("BONUS_COPPER")
			if (iBonus != BonusTypes.NO_BONUS):
				if (pCapitalCity.hasBonus(iBonus)):
					gc.getPlayer(iPlayer).setFeatAccomplished(FeatTypes.FEAT_COPPER_CONNECTED, True)
					
					if (featPopup(iPlayer) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setData1(FeatTypes.FEAT_COPPER_CONNECTED)
						popupInfo.setData2(pCapitalCity.getID())
						popupInfo.setText(localText.getText("TXT_KEY_FEAT_COPPER_CONNECTED", ()))
						popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
						popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
						popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
						popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
						popupInfo.addPopup(iPlayer)

		if (not gc.getPlayer(iPlayer).isFeatAccomplished(FeatTypes.FEAT_HORSE_CONNECTED)):
		
			iBonus = gc.getInfoTypeForString("BONUS_HORSE")
			if (iBonus != BonusTypes.NO_BONUS):
				if (pCapitalCity.hasBonus(iBonus)):
					gc.getPlayer(iPlayer).setFeatAccomplished(FeatTypes.FEAT_HORSE_CONNECTED, True)
					
					if (featPopup(iPlayer) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setData1(FeatTypes.FEAT_HORSE_CONNECTED)
						popupInfo.setData2(pCapitalCity.getID())
						popupInfo.setText(localText.getText("TXT_KEY_FEAT_HORSE_CONNECTED", ()))
						popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
						popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
						popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
						popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
						popupInfo.addPopup(iPlayer)

		if (not gc.getPlayer(iPlayer).isFeatAccomplished(FeatTypes.FEAT_IRON_CONNECTED)):
		
			iBonus = gc.getInfoTypeForString("BONUS_IRON")
			if (iBonus != BonusTypes.NO_BONUS):
				if (pCapitalCity.hasBonus(iBonus)):
					gc.getPlayer(iPlayer).setFeatAccomplished(FeatTypes.FEAT_IRON_CONNECTED, True)
					
					if (featPopup(iPlayer) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setData1(FeatTypes.FEAT_IRON_CONNECTED)
						popupInfo.setData2(pCapitalCity.getID())
						popupInfo.setText(localText.getText("TXT_KEY_FEAT_IRON_CONNECTED", ()))
						popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
						popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
						popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
						popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
						popupInfo.addPopup(iPlayer)

		if (not gc.getPlayer(iPlayer).isFeatAccomplished(FeatTypes.FEAT_LUXURY_CONNECTED)):
		
			for iI in range(gc.getNumBonusInfos()):
				if (gc.getBonusInfo(iI).getHappiness() > 0):
					if (pCapitalCity.hasBonus(iI)):
						gc.getPlayer(iPlayer).setFeatAccomplished(FeatTypes.FEAT_LUXURY_CONNECTED, True)
						
						if (featPopup(iPlayer) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(FeatTypes.FEAT_LUXURY_CONNECTED)
							popupInfo.setData2(pCapitalCity.getID())
							popupInfo.setText(localText.getText("TXT_KEY_FEAT_LUXURY_CONNECTED", (gc.getBonusInfo(iI).getTextKey(), )))
							popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
							popupInfo.addPopup(iPlayer)
						
						break

		if (not gc.getPlayer(iPlayer).isFeatAccomplished(FeatTypes.FEAT_FOOD_CONNECTED)):
		
			for iI in range(gc.getNumBonusInfos()):
				if (gc.getBonusInfo(iI).getHealth() > 0):
					if (pCapitalCity.hasBonus(iI)):
						gc.getPlayer(iPlayer).setFeatAccomplished(FeatTypes.FEAT_FOOD_CONNECTED, True)
						
						if (featPopup(iPlayer) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(FeatTypes.FEAT_FOOD_CONNECTED)
							popupInfo.setData2(pCapitalCity.getID())
							popupInfo.setText(localText.getText("TXT_KEY_FEAT_FOOD_CONNECTED", (gc.getBonusInfo(iI).getTextKey(), )))
							popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
							popupInfo.addPopup(iPlayer)
						
						break

		if (not gc.getPlayer(iPlayer).isFeatAccomplished(FeatTypes.FEAT_CORPORATION_ENABLED)):
		
			for iI in range(gc.getNumBuildingInfos()):
				eCorporation = gc.getBuildingInfo(iI).getFoundsCorporation()
				if eCorporation != -1 and not gc.getGame().isCorporationFounded(eCorporation):
					bValid = true
					eTeam = gc.getPlayer(iPlayer).getTeam()
					if not gc.getTeam(eTeam).isHasTech(gc.getBuildingInfo(iI).getPrereqAndTech()):
						bValid = false
					if bValid:
						for iPrereq in range(gc.getDefineINT("NUM_BUILDING_AND_TECH_PREREQS")):
							if not gc.getTeam(eTeam).isHasTech(gc.getBuildingInfo(iI).getPrereqAndTechs(iPrereq)):
								bValid = false
								break
					if bValid:							
						gc.getPlayer(iPlayer).setFeatAccomplished(FeatTypes.FEAT_CORPORATION_ENABLED, True)
						
						szBonusList = u""
						bFirst = true
						for iPrereq in range(gc.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES")):
							eBonus = gc.getCorporationInfo(eCorporation).getPrereqBonus(iPrereq)
							if eBonus != -1:
								if bFirst:
									bFirst = false
								else:
									szBonusList += localText.getText("TXT_KEY_OR", ())
								szBonusList += gc.getBonusInfo(eBonus).getDescription()
						
						szFounder = u""
						for iUnit in range(gc.getNumUnitInfos()):
							if gc.getUnitInfo(iUnit).getBuildings(iI) or gc.getUnitInfo(iUnit).getForceBuildings(iI):
								szFounder = gc.getUnitInfo(iUnit).getTextKey()
								break
						
						if (featPopup(iPlayer) and (gc.getGame().getStartYear() == gc.getDefineINT("START_YEAR"))):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(FeatTypes.FEAT_CORPORATION_ENABLED)
							popupInfo.setData2(pCapitalCity.getID())
							popupInfo.setText(localText.getText("TXT_KEY_FEAT_CORPORATION_ENABLED", (gc.getCorporationInfo(eCorporation).getTextKey(), szFounder, szBonusList)))
							popupInfo.setOnClickedPythonCallback("featAccomplishedOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("featAccomplishedOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_OK", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_FEAT_ACCOMPLISHED_MORE", ()), "")
							popupInfo.addPopup(iPlayer)
						
						break

def cityAdvise(pCity, iPlayer):

	global g_iAdvisorNags

	if (g_iAdvisorNags >= 2):
		return

	if (pCity.isDisorder()):
		return

	if (gc.getPlayer(iPlayer).isOption(PlayerOptionTypes.PLAYEROPTION_ADVISOR_POPUPS) and gc.getPlayer(iPlayer).isHuman() and not gc.getGame().isNetworkMultiPlayer()):
		
		if (gc.getGame().getGameTurn() % 40 == pCity.getGameTurnFounded() % 40):
			if (not pCity.getID() in g_listNoLiberateCities):
				eLiberationPlayer = pCity.getLiberationPlayer(false)
				if (eLiberationPlayer != -1):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setData1(pCity.getID())
					popupInfo.setText(localText.getText("TXT_KEY_POPUP_LIBERATION_DEMAND", (pCity.getNameKey(), gc.getPlayer(eLiberationPlayer).getCivilizationDescriptionKey(), gc.getPlayer(eLiberationPlayer).getNameKey())))
					popupInfo.setOnClickedPythonCallback("liberateOnClickedCallback")
					popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
					popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
					popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
					popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
					popupInfo.addPopup(iPlayer)
					g_listNoLiberateCities.append(pCity.getID())
					g_iAdvisorNags += 1

				elif (gc.getPlayer(iPlayer).canSplitEmpire() and gc.getPlayer(iPlayer).canSplitArea(pCity.area().getID()) and pCity.AI_cityValue() < 0):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setData1(pCity.getID())
					popupInfo.setText(localText.getText("TXT_KEY_POPUP_COLONY_DEMAND", (pCity.getNameKey(), )))
					popupInfo.setOnClickedPythonCallback("colonyOnClickedCallback")
					popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
					popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
					popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
					popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
					popupInfo.addPopup(iPlayer)
					g_listNoLiberateCities.append(pCity.getID())
					g_iAdvisorNags += 1

		if (pCity.isProduction()):
		
			if (not pCity.isProductionUnit() and (pCity.getOrderQueueLength() <= 1)):

				if (gc.getGame().getGameTurn() + 1) % 40 == pCity.getGameTurnFounded() % 40:
					
					if ((gc.getGame().getElapsedGameTurns() < 200) and (pCity.getPopulation() > 2) and (gc.getPlayer(iPlayer).AI_totalAreaUnitAIs(pCity.area(), UnitAITypes.UNITAI_SETTLE) == 0) and not gc.getPlayer(iPlayer).AI_isFinancialTrouble() and (pCity.area().getBestFoundValue(iPlayer) > 0)):
					
						iBestValue = 0
						eBestUnit = UnitTypes.NO_UNIT

						for iI in range(gc.getNumUnitClassInfos()):

							if (not isLimitedUnitClass(iI)):
								
								eLoopUnit = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationUnits(iI)
								
								if (eLoopUnit != UnitTypes.NO_UNIT):
								
									if (gc.getUnitInfo(eLoopUnit).getDomainType() == DomainTypes.DOMAIN_LAND):

										if pCity.canTrain(eLoopUnit, False, False):

											if (pCity.getFirstUnitOrder(eLoopUnit) == -1):
											
												iValue = gc.getPlayer(iPlayer).AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_SETTLE, pCity.area())

												if (iValue > iBestValue):
												
													iBestValue = iValue
													eBestUnit = eLoopUnit
											
						if (eBestUnit != UnitTypes.NO_UNIT):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_TRAIN)
							popupInfo.setData3(eBestUnit)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_UNIT_SETTLE_DEMAND", (gc.getUnitInfo(eBestUnit).getTextKey(), )))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1
					
				if (gc.getGame().getGameTurn() + 5) % 40 == pCity.getGameTurnFounded() % 40:
					
					if ((pCity.getPopulation() > 1) and (pCity.countNumImprovedPlots() == 0) and (pCity.AI_countBestBuilds(pCity.area()) > 3)):
					
						iBestValue = 0
						eBestUnit = UnitTypes.NO_UNIT

						for iI in range(gc.getNumUnitClassInfos()):

							if (not isLimitedUnitClass(iI)):
								
								eLoopUnit = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationUnits(iI)
								
								if (eLoopUnit != UnitTypes.NO_UNIT):
								
									if (gc.getUnitInfo(eLoopUnit).getDomainType() == DomainTypes.DOMAIN_LAND):

										if pCity.canTrain(eLoopUnit, False, False):

											if (pCity.getFirstUnitOrder(eLoopUnit) == -1):
											
												iValue = gc.getPlayer(iPlayer).AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_WORKER, pCity.area())

												if (iValue > iBestValue):
												
													iBestValue = iValue
													eBestUnit = eLoopUnit
											
						if (eBestUnit != UnitTypes.NO_UNIT):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_TRAIN)
							popupInfo.setData3(eBestUnit)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_UNIT_WORKER_DEMAND", (pCity.getNameKey(), gc.getUnitInfo(eBestUnit).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if (gc.getGame().getGameTurn() + 9) % 40 == pCity.getGameTurnFounded() % 40:
					
					if (pCity.plot().getNumDefenders(iPlayer) == 0):
					
						iBestValue = 0
						eBestUnit = UnitTypes.NO_UNIT

						for iI in range(gc.getNumUnitClassInfos()):

							if (not isLimitedUnitClass(iI)):
								
								eLoopUnit = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationUnits(iI)
								
								if (eLoopUnit != UnitTypes.NO_UNIT):
								
									if (gc.getUnitInfo(eLoopUnit).getDomainType() == DomainTypes.DOMAIN_LAND):

										if pCity.canTrain(eLoopUnit, False, False):

											iValue = (gc.getPlayer(iPlayer).AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_CITY_DEFENSE, pCity.area()) * 2)
											iValue += gc.getPlayer(iPlayer).AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_ATTACK, pCity.area())

											if (iValue > iBestValue):
											
												iBestValue = iValue
												eBestUnit = eLoopUnit
										
						if (eBestUnit != UnitTypes.NO_UNIT):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_TRAIN)
							popupInfo.setData3(eBestUnit)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_UNIT_DEFENSE_DEMAND", (pCity.getNameKey(), gc.getUnitInfo(eBestUnit).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if (gc.getGame().getGameTurn() + 12) % 40 == pCity.getGameTurnFounded() % 40:
					
					if ((gc.getPlayer(iPlayer).AI_totalAreaUnitAIs(pCity.area(), UnitAITypes.UNITAI_MISSIONARY) == 0) and (gc.getTeam(gc.getPlayer(iPlayer).getTeam()).getAtWarCount(True) == 0)):
					
						eStateReligion = gc.getPlayer(iPlayer).getStateReligion()
						
						if (eStateReligion != ReligionTypes.NO_RELIGION):
						
							if (gc.getPlayer(iPlayer).getHasReligionCount(eStateReligion) < (gc.getPlayer(iPlayer).getNumCities() / 2)):
							
								iBestValue = 0
								eBestUnit = UnitTypes.NO_UNIT

								for iI in range(gc.getNumUnitClassInfos()):

									eLoopUnit = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationUnits(iI)
									
									if (eLoopUnit != UnitTypes.NO_UNIT):
									
										if (gc.getUnitInfo(eLoopUnit).getDomainType() == DomainTypes.DOMAIN_LAND):

											if (gc.getUnitInfo(eLoopUnit).getReligionSpreads(eStateReligion)):
											
												if pCity.canTrain(eLoopUnit, False, False):

													iValue = gc.getPlayer(iPlayer).AI_unitValue(eLoopUnit, UnitAITypes.UNITAI_MISSIONARY, pCity.area())

													if (iValue > iBestValue):
													
														iBestValue = iValue
														eBestUnit = eLoopUnit
												
								if (eBestUnit != UnitTypes.NO_UNIT):
									popupInfo = CyPopupInfo()
									popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
									popupInfo.setData1(pCity.getID())
									popupInfo.setData2(OrderTypes.ORDER_TRAIN)
									popupInfo.setData3(eBestUnit)
									popupInfo.setText(localText.getText("TXT_KEY_POPUP_MISSIONARY_DEMAND", (gc.getReligionInfo(eStateReligion).getTextKey(), gc.getUnitInfo(eBestUnit).getTextKey(), pCity.getNameKey())))
									popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
									popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
									popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
									popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
									popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
									popupInfo.addPopup(iPlayer)
									g_iAdvisorNags += 1

			if (not pCity.isProductionBuilding() and (pCity.getOrderQueueLength() <= 1)):

				if (pCity.healthRate(False, 0) < 0):
				
					if (gc.getGame().getGameTurn() + 2) % 40 == pCity.getGameTurnFounded() % 40:
							
						iBestValue = 0
						eBestBuilding = BuildingTypes.NO_BUILDING

						for iI in range(gc.getNumBuildingClassInfos()):

							if (not isLimitedWonderClass(iI)):
							
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iI)
								
								if (eLoopBuilding != BuildingTypes.NO_BUILDING):
								
									if (gc.getBuildingInfo(eLoopBuilding).getHealth() > 0):

										if pCity.canConstruct(eLoopBuilding, False, False, False):

											iValue = gc.getBuildingInfo(eLoopBuilding).getHealth()

											if (iValue > iBestValue):
											
												iBestValue = iValue
												eBestBuilding = eLoopBuilding
										
						if (eBestBuilding != BuildingTypes.NO_BUILDING):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
							popupInfo.setData3(eBestBuilding)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_UNHEALTHY_CITIZENS_DEMAND", (pCity.getNameKey(), gc.getBuildingInfo(eBestBuilding).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_UNHEALTHY_DO_SO_NEXT", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_UNHEALTHY_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_UNHEALTHY_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if (pCity.angryPopulation(0) > 0):

					if (gc.getGame().getGameTurn() + 3) % 40 == pCity.getGameTurnFounded() % 40:

						iBestValue = 0
						eBestBuilding = BuildingTypes.NO_BUILDING

						for iI in range(gc.getNumBuildingClassInfos()):

							if (not isLimitedWonderClass(iI)):
							
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iI)
								
								if (eLoopBuilding != BuildingTypes.NO_BUILDING):
								
									if (gc.getBuildingInfo(eLoopBuilding).getHappiness() > 0):

										if pCity.canConstruct(eLoopBuilding, False, False, False):

											iValue = gc.getBuildingInfo(eLoopBuilding).getHappiness()

											if (iValue > iBestValue):

												iBestValue = iValue
												eBestBuilding = eLoopBuilding

						if (eBestBuilding != BuildingTypes.NO_BUILDING):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
							popupInfo.setData3(eBestBuilding)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_UNHAPPY_CITIZENS_DEMAND", (pCity.getNameKey(), gc.getBuildingInfo(eBestBuilding).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_UNHAPPY_DO_SO_NEXT", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_UNHAPPY_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_UNHEALTHY_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if ((gc.getGame().getGameTurn < 100) and (gc.getTeam(gc.getPlayer(iPlayer).getTeam()).getHasMetCivCount(True) > 0) and (pCity.getBuildingDefense() == 0)):
				
					if (gc.getGame().getGameTurn() + 4) % 40 == pCity.getGameTurnFounded() % 40:

						iBestValue = 0
						eBestBuilding = BuildingTypes.NO_BUILDING

						for iI in range(gc.getNumBuildingClassInfos()):

							if (not isLimitedWonderClass(iI)):
							
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iI)
								
								if (eLoopBuilding != BuildingTypes.NO_BUILDING):
								
									if (gc.getBuildingInfo(eLoopBuilding).getDefenseModifier() > pCity.getNaturalDefense()):

										if pCity.canConstruct(eLoopBuilding, False, False, False):

											iValue = gc.getBuildingInfo(eLoopBuilding).getDefenseModifier()

											if (iValue > iBestValue):
											
												iBestValue = iValue
												eBestBuilding = eLoopBuilding
										
						if (eBestBuilding != BuildingTypes.NO_BUILDING):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
							popupInfo.setData3(eBestBuilding)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_BUILDING_DEFENSE_DEMAND", (pCity.getNameKey(), gc.getBuildingInfo(eBestBuilding).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if (pCity.getMaintenance() >= 8):
				
					if (gc.getGame().getGameTurn() + 6) % 40 == pCity.getGameTurnFounded() % 40:

						iBestValue = 0
						eBestBuilding = BuildingTypes.NO_BUILDING

						for iI in range(gc.getNumBuildingClassInfos()):

							if (not isLimitedWonderClass(iI)):
							
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iI)
								
								if (eLoopBuilding != BuildingTypes.NO_BUILDING):
								
									if (gc.getBuildingInfo(eLoopBuilding).getMaintenanceModifier() < 0):

										if pCity.canConstruct(eLoopBuilding, False, False, False):

											iValue = gc.getBuildingInfo(eLoopBuilding).getMaintenanceModifier()

											if (iValue < iBestValue):
											
												iBestValue = iValue
												eBestBuilding = eLoopBuilding
										
						if (eBestBuilding != BuildingTypes.NO_BUILDING):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
							popupInfo.setData3(eBestBuilding)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_MAINTENANCE_DEMAND", (pCity.getNameKey(), gc.getBuildingInfo(eBestBuilding).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if (pCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE) == 0 and not pCity.isOccupation()):
				
					if (gc.getGame().getGameTurn() + 7) % 40 == pCity.getGameTurnFounded() % 40:

						iBestValue = 0
						eBestBuilding = BuildingTypes.NO_BUILDING

						for iI in range(gc.getNumBuildingClassInfos()):

							if (not isLimitedWonderClass(iI)):
							
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iI)
								
								if (eLoopBuilding != BuildingTypes.NO_BUILDING):
								
									if (gc.getBuildingInfo(eLoopBuilding).getObsoleteSafeCommerceChange(CommerceTypes.COMMERCE_CULTURE) > 0):

										if pCity.canConstruct(eLoopBuilding, False, False, False):

											iValue = gc.getBuildingInfo(eLoopBuilding).getObsoleteSafeCommerceChange(CommerceTypes.COMMERCE_CULTURE)

											if (iValue > iBestValue):
											
												iBestValue = iValue
												eBestBuilding = eLoopBuilding
										
						if (eBestBuilding != BuildingTypes.NO_BUILDING):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
							popupInfo.setData3(eBestBuilding)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_CULTURE_DEMAND", (pCity.getNameKey(), gc.getBuildingInfo(eBestBuilding).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if (pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_GOLD) > 10):
				
					if (gc.getGame().getGameTurn() + 8) % 40 == pCity.getGameTurnFounded() % 40:

						iBestValue = 0
						eBestBuilding = BuildingTypes.NO_BUILDING

						for iI in range(gc.getNumBuildingClassInfos()):

							if (not isLimitedWonderClass(iI)):
							
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iI)
								
								if (eLoopBuilding != BuildingTypes.NO_BUILDING):
								
									if (gc.getBuildingInfo(eLoopBuilding).getCommerceModifier(CommerceTypes.COMMERCE_GOLD) > 0):

										if pCity.canConstruct(eLoopBuilding, False, False, False):

											iValue = gc.getBuildingInfo(eLoopBuilding).getCommerceModifier(CommerceTypes.COMMERCE_GOLD)

											if (iValue > iBestValue):
											
												iBestValue = iValue
												eBestBuilding = eLoopBuilding
										
						if (eBestBuilding != BuildingTypes.NO_BUILDING):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
							popupInfo.setData3(eBestBuilding)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_GOLD_DEMAND", (pCity.getNameKey(), gc.getBuildingInfo(eBestBuilding).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if (pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_RESEARCH) > 10):
				
					if (gc.getGame().getGameTurn() + 10) % 40 == pCity.getGameTurnFounded() % 40:

						iBestValue = 0
						eBestBuilding = BuildingTypes.NO_BUILDING

						for iI in range(gc.getNumBuildingClassInfos()):

							if (not isLimitedWonderClass(iI)):
							
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iI)
								
								if (eLoopBuilding != BuildingTypes.NO_BUILDING):
								
									if (gc.getBuildingInfo(eLoopBuilding).getCommerceModifier(CommerceTypes.COMMERCE_RESEARCH) > 0):

										if pCity.canConstruct(eLoopBuilding, False, False, False):

											iValue = gc.getBuildingInfo(eLoopBuilding).getCommerceModifier(CommerceTypes.COMMERCE_RESEARCH)

											if (iValue > iBestValue):
											
												iBestValue = iValue
												eBestBuilding = eLoopBuilding
										
						if (eBestBuilding != BuildingTypes.NO_BUILDING):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
							popupInfo.setData3(eBestBuilding)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_RESEARCH_DEMAND", (pCity.getNameKey(), gc.getBuildingInfo(eBestBuilding).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1

				if (pCity.countNumWaterPlots() > 10):
				
					if (gc.getGame().getGameTurn() + 11) % 40 == pCity.getGameTurnFounded() % 40:

						iBestValue = 0
						eBestBuilding = BuildingTypes.NO_BUILDING

						for iI in range(gc.getNumBuildingClassInfos()):

							if (not isLimitedWonderClass(iI)):
							
								eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationBuildings(iI)
								
								if (eLoopBuilding != BuildingTypes.NO_BUILDING):
								
									if (gc.getBuildingInfo(eLoopBuilding).getSeaPlotYieldChange(YieldTypes.YIELD_FOOD) > 0):

										if pCity.canConstruct(eLoopBuilding, False, False, False):

											iValue = gc.getBuildingInfo(eLoopBuilding).getSeaPlotYieldChange(YieldTypes.YIELD_FOOD)

											if (iValue > iBestValue):
											
												iBestValue = iValue
												eBestBuilding = eLoopBuilding
										
						if (eBestBuilding != BuildingTypes.NO_BUILDING):
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(OrderTypes.ORDER_CONSTRUCT)
							popupInfo.setData3(eBestBuilding)
							popupInfo.setText(localText.getText("TXT_KEY_POPUP_WATER_FOOD_DEMAND", (pCity.getNameKey(), gc.getBuildingInfo(eBestBuilding).getTextKey())))
							popupInfo.setOnClickedPythonCallback("cityWarningOnClickedCallback")
							popupInfo.setOnFocusPythonCallback("cityWarningOnFocusCallback")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_AGREE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_REFUSE", ()), "")
							popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_DEMAND_EXAMINE", ()), "")
							popupInfo.addPopup(iPlayer)
							g_iAdvisorNags += 1
