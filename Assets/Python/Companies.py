from CvPythonExtensions import *

from Core import *
from Locations import *
from Events import handler


dCompanyTechs = {
	iSilkRoute        : [iCurrency],
	iTradingCompany   : [iExploration],
	iCerealIndustry   : [iEconomics, iBiology],
	iFishingIndustry  : [iEconomics, iRefrigeration],
	iTextileIndustry  : [iEconomics, iThermodynamics],
	iSteelIndustry    : [iEconomics, iMetallurgy],
	iOilIndustry      : [iEconomics, iRefining],
	iLuxuryIndustry   : [iEconomics, iConsumerism],
	iComputerIndustry : [iEconomics, iComputers],
}

tCompaniesLimit = (10, 12, 16, 10, 12, 12, 6, 10, 12) # kind of arbitrary currently, see how this plays out

dCompanyExpiry = defaultdict({
	iSilkRoute : 1500,
	iTradingCompany : 1800,
	iTextileIndustry : 1920,
}, 2020)
					
	
@handler("cityAcquired")
def verifyCorporations(iOwner, iPlayer, city):
	for iCorporation in range(iNumCorporations):
		if city.isHasCorporation(iCorporation):
			if getCityValue(city, iCorporation) < 0:
				city.setHasCorporation(iCorporation, False, True, True)


@handler("BeginGameTurn")
def checkCompanies(iGameTurn):
	for iCompany in infos.corporations().periodic_iter(iNumCorporations / 2):
		checkCompany(iCompany, iGameTurn)


def isCompanyValid(iCompany, iGameTurn):
	return iGameTurn <= year(dCompanyExpiry[iCompany])


def getCompanyLimit(iCompany, iGameTurn):
	if not isCompanyValid(iCompany, iGameTurn):
		return 0
	
	return tCompaniesLimit[iCompany]
	
	
def canHaveCompany(iCompany, iPlayer):
	return all(team(iPlayer).isHasTech(iTech) for iTech in dCompanyTechs[iCompany])
	

def checkCompany(iCompany, iGameTurn):
	iMaxCompanies = getCompanyLimit(iCompany, iGameTurn)
		
	# count the number of companies
	iCompanyCount = players.major().alive().sum(lambda p: player(p).countCorporations(iCompany))
			
	# return if gameturn is beyond company fall date and removed from all cities
	if iMaxCompanies == 0 and iCompanyCount == 0:
		return
	
	# select all cities for players that can have the company
	positiveCities, negativeCities = players.major().where(lambda p: canHaveCompany(iCompany, p)).cities().split(lambda city: getCityValue(city, iCompany) > player(city).countCorporations(iCompany) * 2)
	
	# remove from cities with negative value
	for city in negativeCities.corporation(iCompany).sort(lambda city: getCityValue(city, iCompany), True):
		if getCityValue(city, iCompany) <= player(city).countCorporations(iCompany) * 2:
			city.setHasCorporation(iCompany, False, True, True)
	
	companyCities, availableCities = positiveCities.split(lambda city: city.isHasCorporation(iCompany))
	
	# if company can still spread, select the most attractive city without the company
	if iCompanyCount < iMaxCompanies:
		city = availableCities.maximum(lambda city: getCityValue(city, iCompany) * 10 + rand(10))
		if city:
			city.setHasCorporation(iCompany, True, True, True)
	
	# if too many cities have the company, remove it from the least attractive city that has it
	elif iCompanyCount > iMaxCompanies:
		city = companyCities.minimum(lambda city: getCityValue(city, iCompany) * 10 + rand(10))
		if city:
			city.setHasCorporation(iCompany, False, True, True)


def getCityValue(city, iCompany):
	iValue = 2
	
	iOwner = city.getOwner()
	iOwnerCiv = civ(iOwner)
	owner = player(city)
	ownerTeam = team(city)
	
	# Central Planning: only one company per city
	if has_civic(owner, iCentralPlanning):
		for iLoopCorporation in range(iNumCorporations):
			if city.isHasCorporation(iLoopCorporation) and iLoopCorporation != iCompany:
				return -1

	# Colonialism increases likeliness for trading company
	if iCompany == iTradingCompany and has_civic(owner, iColonialism):
		iValue += 2
		
	# Merchant Trade increases likeliness for silk route
	if iCompany == iSilkRoute and has_civic(owner, iMerchantTrade):
		iValue += 2

	# Free Enterprise increases likeliness for all companies
	if has_civic(owner, iFreeEnterprise):
		iValue += 1

	# civilization requirements
	if iCompany == iTradingCompany:
		if iOwnerCiv not in dTradingCompanyPlots:
			return -1
		if iOwnerCiv == iNetherlands:
			iValue += 2
	elif iCompany == iSilkRoute:
		if city.getRegionID() in [rCentralAsia, rPersia]:
			iValue += 2
		elif city.getRegionID() == rChina:
			iValue -= 2
	
	# geographical requirements
	if iCompany == iSilkRoute:
		if city not in cities.rectangle(tSilkRoute) and city not in cities.rectangle(tMiddleEast).without(lMiddleEastExceptions):
			return -1
			
	elif iCompany == iTradingCompany:
		if city not in cities.rectangle(tCaribbean) and city not in cities.rectangle(tSubSaharanAfrica) and city not in cities.rectangle(tSouthAsia) and not city.isHasRealBuilding(unique_building(city.getOwner(), iTradingCompanyBuilding)):
			return -1
		if city in cities.rectangle(tCaribbean):
			iValue += 1
	
	# trade companies and fishing industry - coastal cities only
	if iCompany in [iTradingCompany, iFishingIndustry]:
		if not city.isCoastal(20):
			return -1

	# penalty for silk route if coastal (mitigatable by harbor)
	if iCompany == iSilkRoute:
		if city.isCoastal(20):
			iValue -= 1
	
	# religions
	if iCompany == iSilkRoute:
		if owner.getStateReligion() in [iProtestantism, iCatholicism, iOrthodoxy]:
			iValue -= 1
	
	# various bonuses
	if iCompany == iSilkRoute:
		if city.hasBuilding(unique_building(iOwner, iWeaver)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iMarket)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iStable)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iHarbor)): iValue += 1

	elif iCompany == iTradingCompany:
		if city.hasBuilding(unique_building(iOwner, iHarbor)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iCustomsHouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iBank)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iTradingCompanyBuilding)): iValue += 2

	elif iCompany == iCerealIndustry:
		if city.hasBuilding(unique_building(iOwner, iGranary)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSewer)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSupermarket)): iValue += 1

	elif iCompany == iFishingIndustry:
		if city.hasBuilding(unique_building(iOwner, iLighthouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iHarbor)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSupermarket)): iValue += 1
		
	elif iCompany == iTextileIndustry:
		if city.hasBuilding(unique_building(iOwner, iMarket)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWeaver)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1

	elif iCompany == iSteelIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iCoalPlant)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iIndustrialPark)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iIronworks)): iValue += 3

	elif iCompany == iOilIndustry:
		if city.hasBuilding(unique_building(iOwner, iBank)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iDistillery)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iIndustrialPark)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iStockExchange)): iValue += 3

	elif iCompany == iLuxuryIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWeaver)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iDepartmentStore)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iNationalGallery)): iValue += 3

	elif iCompany == iComputerIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iLaboratory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iUniversity)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iCERN)): iValue += 3

	# trade routes
	iValue += city.getTradeRoutes() - 1
	
	# resources
	iTempValue = 0
	bFound = False
	for i in range(6):
		iBonus = infos.corporation(iCompany).getPrereqBonus(i)
		if iBonus > -1:
			if city.getNumBonuses(iBonus) > 0: 
				bFound = True
				if iCompany in [iFishingIndustry, iCerealIndustry, iTextileIndustry]:
					iTempValue += city.getNumBonuses(iBonus)
				elif iCompany == iOilIndustry:
					iTempValue += city.getNumBonuses(iBonus) * 4
				elif iCompany == iSilkRoute:
					if iBonus == iSilk:
						iTempValue += city.getNumBonuses(iBonus) * 4
					else:
						iTempValue += city.getNumBonuses(iBonus) * 2
				else:
					iTempValue += city.getNumBonuses(iBonus) * 2
	
	# Brazilian UP: sugar counts as oil for Oil Industry
	if iOwnerCiv == iBrazil and iCompany == iOilIndustry:
		if city.getNumBonuses(iSugar) > 0:
			bFound = True
			iTempValue += city.getNumBonuses(iSugar) * 3
				
	if not bFound: 
		return -1
	
	iValue += iTempValue
	
	# competition
	if iCompany == iCerealIndustry and city.isHasCorporation(iFishingIndustry): iValue /= 2
	elif iCompany == iFishingIndustry and city.isHasCorporation(iCerealIndustry): iValue /= 2
	elif iCompany == iSteelIndustry and city.isHasCorporation(iTextileIndustry): iValue /= 2
	elif iCompany == iTextileIndustry and city.isHasCorporation(iSteelIndustry): iValue /= 2
	elif iCompany == iOilIndustry and city.isHasCorporation(iComputerIndustry): iValue /= 2
	elif iCompany == iComputerIndustry and city.isHasCorporation(iOilIndustry): iValue /= 2
	
	# threshold
	if iValue < 4:
		return -1
	
	return iValue