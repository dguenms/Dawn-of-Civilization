from Core import *


lCityStatesStart = [iRome, iCarthage, iGreece, iIndia, iMaya, iAztecs]


def isCommunist(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iLegitimacy == iVassalage:
		return False
	
	if civic.iEconomy == iCentralPlanning:
		return True
	
	if civic.iGovernment == iStateParty and civic.iSociety != iTotalitarianism and civic.iEconomy not in [iMerchantTrade, iFreeEnterprise]:
		return True
		
	return False
	
def isFascist(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iSociety == iTotalitarianism:
		return True
	
	if civic.iGovernment == iStateParty:
		return True
		
	return False
	
def isRepublic(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iGovernment == iDemocracy:
		return True
	
	if civic.iGovernment in [iDespotism, iRepublic, iElective] and civic.iLegitimacy == iConstitution:
		return True
	
	return False
	
def isCityStates(iPlayer):
	civic = civics(iPlayer)
	
	if civic.iLegitimacy not in [iAuthority, iCitizenship, iCentralism]:
		return False
	
	if civic.iGovernment in [iRepublic, iElective, iDemocracy]:
		return True
	
	if civic.iGovernment == iChiefdom and civ(iPlayer) in lCityStatesStart:
		return True
	
	return False