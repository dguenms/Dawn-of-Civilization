from CvPythonExtensions import *

from Core import *
from Locations import *
from Events import handler


dCompanyTechs = {
	iSilkRoute          : (iCurrency,),
	iTradingCompany     : (iExploration,),
	iCerealIndustry     : (iEconomics, iBiology),
	iFishingIndustry    : (iEconomics, iRefrigeration),
	iTextileIndustry    : (iEconomics, iThermodynamics),
	iSteelIndustry      : (iEconomics, iMetallurgy),
	iOilIndustry        : (iEconomics, iRefining),
	iLuxuryIndustry     : (iEconomics, iConsumerism),
	iAutomobileIndustry : (iEconomics, iInfrastructure),
	iComputerIndustry   : (iEconomics, iComputers),
}

tCompaniesLimit = (20, 25, 30, 20, 25, 25, 15, 20, 20, 25) # kind of arbitrary currently, see how this plays out

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
	for iCompany in infos.corporations().periodic_iter(iNumCorporations / 3):
		checkCompany(iCompany, iGameTurn)


def isCompanyValid(iCompany):
	return turn() <= year(dCompanyExpiry[iCompany])


def getCompanyLimit(iCompany):
	if not isCompanyValid(iCompany):
		return 0
	
	iEnabledCount = players.major().existing().count(lambda p: canHaveCompany(iCompany, p))
	
	return min(3 * iEnabledCount, tCompaniesLimit[iCompany])
	
	
def canHaveCompany(iCompany, iPlayer):
	return all(team(iPlayer).isHasTech(iTech) for iTech in dCompanyTechs[iCompany])
	

def checkCompany(iCompany, iGameTurn):
	iMaxCompanies = getCompanyLimit(iCompany)
		
	# count the number of companies
	iCompanyCount = players.major().existing().sum(lambda p: player(p).countCorporations(iCompany))
			
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
	
	# if at maximum, remove from the least attractive city and spread it to the most attractive city if their difference is large enough
	else:
		removeCity = companyCities.minimum(lambda city: getCityValue(city, iCompany))
		spreadCity = availableCities.maximum(lambda city: getCityValue(city, iCompany))
		if removeCity and spreadCity:
			if getCityValue(spreadCity, iCompany) > getCityValue(removeCity, iCompany) + 5:
				removeCity.setHasCorporation(iCompany, False, True, True)
				spreadCity.setHasCorporation(iCompany, True, True, True)
				


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
		if iOwnerCiv not in dCivGroups[iCivGroupEurope]:
			return -1
		if iOwnerCiv == iNetherlands:
			iValue += 2
	elif iCompany == iSilkRoute:
		if city.getRegionID() in [rTarimBasin, rTransoxiana, rHinduKush, rKhorasan, rPersia]:
			iValue += 2
		elif city.getRegionID() in [rSouthChina, rNorthChina]:
			iValue -= 2
	
	# geographical requirements
	if iCompany == iSilkRoute:
		if city.getRegionID() not in [rMongolia, rTarimBasin, rTransoxiana, rKhorasan, rHinduKush, rPersia, rMesopotamia, rLevant]:
			return -1
			
	elif iCompany == iTradingCompany:
		if not city.isHasRealBuilding(unique_building(city.getOwner(), iTradingCompanyBuilding)):
			if city.getRegionID() not in [rCaribbean, rArabia, rDeccan, rDravida, rBengal, rIndochina, rIndonesia, rPhilippines] + lSubSaharanAfrica:
				return -1
			
			if not city.isCoastal(20):
				return -1
	
		if city.getRegionID() == rCaribbean:
			iValue += 1
	
	# fishing industry - coastal cities only
	if iCompany == iFishingIndustry:
		if not city.isCoastal(20):
			return -1
	
	# automobile industry - only with oil
	if iCompany == iAutomobileIndustry:
		if city.getNumBonuses(iOil) == 0:
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
		if city.hasBuilding(unique_building(iOwner, iPostOffice)): iValue += 1
		
		if city.isHasBuildingEffect(iSalsalBuddha): iValue += 2
		
		if owner.isHasBuildingEffect(iSalsalBuddha): iValue += 1
		if owner.isHasBuildingEffect(iSanMarcoBasilica): iValue += 1
		if owner.isHasBuildingEffect(iSilverTreeFountain): iValue += 1

	elif iCompany == iTradingCompany:
		if city.hasBuilding(unique_building(iOwner, iHarbor)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iCoffeehouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iCustomsHouse)): iValue += 1
		if city.hasBuilding(iFeitoria): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iBank)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWarehouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iTradingCompanyBuilding)): iValue += 2
		
		if city.isHasBuildingEffect(iBourse): iValue += 2
		if city.isHasBuildingEffect(iTorreDeBelem): iValue += 2
		
		if owner.isHasBuildingEffect(iBourse): iValue += 1
		if owner.isHasBuildingEffect(iTorreDeBelem): iValue += 1

	elif iCompany == iCerealIndustry:
		if city.hasBuilding(unique_building(iOwner, iGranary)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iGrocer)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iGrainSilo)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSupermarket)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iVerticalFarm)): iValue += 1
		
		if city.isHasBuildingEffect(iFloralisGenerica): iValue += 2
		if city.isHasBuildingEffect(iGlobalSeedVault): iValue += 2
		
		if owner.isHasBuildingEffect(iFloralisGenerica): iValue += 1
		if owner.isHasBuildingEffect(iGlobalSeedVault): iValue += 1

	elif iCompany == iFishingIndustry:
		if city.hasBuilding(unique_building(iOwner, iLighthouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iHarbor)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWharf)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iAbattoir)): iValue += 1
		if city.hasBuilding(iColdStoragePlant): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSupermarket)): iValue += 1
		
		if city.isHasBuildingEffect(iBellRockLighthouse): iValue += 2
		if city.isHasBuildingEffect(iTsukijiFishMarket): iValue += 2
		
		if owner.isHasBuildingEffect(iBellRockLighthouse): iValue += 1
		if owner.isHasBuildingEffect(iTsukijiFishMarket): iValue += 1
		
	elif iCompany == iTextileIndustry:
		if city.hasBuilding(unique_building(iOwner, iMarket)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWeaver)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iWarehouse)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iManufactory)): iValue += 2

	elif iCompany == iSteelIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iCoalPlant)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iRailwayStation)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iIndustrialPark)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iIronworks)): iValue += 3
		
		if city.isHasBuildingEffect(iEiffelTower): iValue += 2
		if city.isHasBuildingEffect(iCrystalPalace): iValue += 2
		if city.isHasBuildingEffect(iAtomium): iValue += 2
		
		if owner.isHasBuildingEffect(iEiffelTower): iValue += 1
		if owner.isHasBuildingEffect(iCrystalPalace): iValue += 1
		if owner.isHasBuildingEffect(iAtomium): iValue += 1

	elif iCompany == iOilIndustry:
		if city.hasBuilding(unique_building(iOwner, iBank)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iDistillery)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iIndustrialPark)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iContainerTerminal)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iStockExchange)): iValue += 3
		
		if city.isHasBuildingEffect(iBurjKhalifa): iValue += 2
		
		if owner.isHasBuildingEffect(iBurjKhalifa): iValue += 1

	elif iCompany == iLuxuryIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iJeweller)): iValue += 1
		if city.hasBuilding(iArtStudio): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iDepartmentStore)): iValue += 1
		if city.hasBuilding(iMall): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iHotel)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iNationalGallery)): iValue += 3
	
	elif iCompany == iAutomobileIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iIndustrialPark)): iValue += 2
		if city.hasBuilding(iAssemblyPlant): iValue += 1
		if city.hasBuilding(iZaibatsu): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iPublicTransportation)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iAutomatedFactory)): iValue += 2
		if city.hasBuilding(unique_building(iOwner, iIronworks)): iValue += 3

	elif iCompany == iComputerIndustry:
		if city.hasBuilding(unique_building(iOwner, iFactory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iLaboratory)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iUniversity)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iSupercomputer)): iValue += 1
		if city.hasBuilding(unique_building(iOwner, iFiberNetwork)): iValue += 1
		
		if city.isHasBuildingEffect(iMenloPark): iValue += 2
		if city.isHasBuildingEffect(iCERN): iValue += 2
		if city.isHasBuildingEffect(iGoldenGateBridge): iValue += 2
		if city.isHasBuildingEffect(iOrientalPearlTower): iValue += 2
		if city.isHasBuildingEffect(iSkytree): iValue += 2
		
		if owner.isHasBuildingEffect(iMenloPark): iValue += 1
		if owner.isHasBuildingEffect(iCERN): iValue += 1
		if owner.isHasBuildingEffect(iGoldenGateBridge): iValue += 1
		if owner.isHasBuildingEffect(iOrientalPearlTower): iValue += 1
		if owner.isHasBuildingEffect(iSkytree): iValue += 1
	
	if city.isHasBuildingEffect(iWorldTradeCenter): iValue += 2
	if owner.isHasBuildingEffect(iWorldTradeCenter): iValue += 1
	
	# needs at least a few requirements
	if iValue <= 0:
		return -1

	# trade routes
	iValue += city.getTradeRoutes() - 1
	
	# resources
	iResourceValue = 0
	for i in range(6):
		iBonus = infos.corporation(iCompany).getPrereqBonus(i)
		if iBonus > -1:
			if city.getNumBonuses(iBonus) > 0: 
				if iCompany in [iFishingIndustry, iCerealIndustry, iTextileIndustry]:
					iResourceValue += city.getNumBonuses(iBonus)
				elif iCompany == iOilIndustry:
					iResourceValue += city.getNumBonuses(iBonus) * 4
				elif iCompany == iSilkRoute:
					if iBonus == iSilk:
						iResourceValue += city.getNumBonuses(iBonus) * 4
					else:
						iResourceValue += city.getNumBonuses(iBonus) * 2
				elif iCompany == iAutomobileIndustry:
					if iBonus == iRubber:
						iResourceValue += city.getNumBonuses(iBonus) * 4
					else:
						iResourceValue += city.getNumBonuses(iBonus) * 2
				else:
					iResourceValue += city.getNumBonuses(iBonus) * 2
	
	if iCompany == iAutomobileIndustry:
		iResourceValue += city.getNumBonuses(iOil)
				
	if iResourceValue == 0: 
		return -1
		
	iCompanyCount = player(iOwner).countCorporations(iCompany)
	iCompanyLimit = getCompanyLimit(iCompany)
	
	iCompanyExcess = max(0, iCompanyCount - iCompanyLimit / 2)
	
	iResourceValue /= (1 + iCompanyExcess / 2)
	
	iValue += iResourceValue
	
	# competition
	if iCompany == iCerealIndustry and city.isHasCorporation(iFishingIndustry): iValue /= 2
	elif iCompany == iFishingIndustry and city.isHasCorporation(iCerealIndustry): iValue /= 2
	elif iCompany == iSteelIndustry and (city.isHasCorporation(iTextileIndustry) or city.isHasCorporation(iAutomobileIndustry)): iValue /= 2
	elif iCompany == iTextileIndustry and city.isHasCorporation(iSteelIndustry): iValue /= 2
	elif iCompany == iOilIndustry and (city.isHasCorporation(iComputerIndustry) or city.isHasCorporation(iAutomobileIndustry)): iValue /= 2
	elif iCompany == iAutomobileIndustry and (city.isHasCorporation(iSteelIndustry) or city.isHasCorporation(iOilIndustry)): iValue /= 2
	elif iCompany == iComputerIndustry and city.isHasCorporation(iOilIndustry): iValue /= 2
	
	# threshold
	if iValue < 4:
		return -1
	
	if iCompanyCount > iCompanyLimit / 2: 
		iValue /= 2
	elif iCompanyCount > iCompanyLimit / 4: 
		iValue *= 2
		iValue /= 3
		
	return iValue