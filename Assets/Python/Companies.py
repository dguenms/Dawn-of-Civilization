# The Sword of Islam - Companies

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
from RFCUtils import *
from operator import itemgetter


tCompanyTechs = (iCurrency, iExploration, iBiology, iRefrigeration, iThermodynamics, iMetallurgy, iRefining, iConsumerism, iComputers)
tCompaniesLimit = (10, 12, 16, 10, 12, 12, 6, 10, 12) # kind of arbitrary currently, see how this plays out

lTradingCompanyCivs = [iSpain, iFrance, iEngland, iPortugal, iNetherlands, iVikings] # Vikings too now

tSilkRouteTL = (80, 46)
tSilkRouteBR = (99, 52)

tMiddleEastTL = (68, 38)
tMiddleEastBR = (85, 46)

lMiddleEastExceptions = [(68, 39), (69, 39), (71, 40)]

tCaribbeanTL = (26, 33)
tCaribbeanBR = (34, 39)

tSubSaharanAfricaTL = (49, 10)
tSubSaharanAfricaBR = (77, 29)

tSouthAsiaTL = (76, 24)
tSouthAsiaBR = (117, 39)

class Companies:

	def checkTurn(self, iGameTurn):

		iCompany = iGameTurn % iNumCorporations
		self.checkCompany(iCompany, iGameTurn)

		iCompany = (iGameTurn + 4) % iNumCorporations
		self.checkCompany(iCompany, iGameTurn)


	def checkCompany(self, iCompany, iGameTurn):
		if (iCompany == iSilkRoute and iGameTurn > year(1500)) or (iCompany == iTradingCompany and iGameTurn > year(1800)) or (iCompany == iTextileIndustry and iGameTurn > year(1920)):
			iMaxCompanies = 0
		else:
			iMaxCompanies = tCompaniesLimit[iCompany]
			
		# count the number of companies
		iCompanyCount = 0
		for iLoopPlayer in players.major().alive():
			iCompanyCount += player(iLoopPlayer).countCorporations(iCompany)
				
		# return if gameturn is beyond company fall date and removed from all cities
		if iMaxCompanies == 0 and iCompanyCount == 0:
			return
			
		# loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
		cityValueList = []
		for iPlayer in players.major():
			if team(iPlayer).isHasTech(tCompanyTechs[iCompany]) and (team(iPlayer).isHasTech(iEconomics) or iCompany <= iTradingCompany):
				for city in cities.owner(iPlayer):
					iValue = self.getCityValue(city, iCompany)
					if iValue > 0: 
						cityValueList.append((city, iValue * 10 + rand(10)))
					elif city.isHasCorporation(iCompany): # quick check to remove companies
						city.setHasCorporation(iCompany, False, True, True)
						
		# sort cities from highest to lowest value
		cityValueList.sort(key=itemgetter(1), reverse=True)
		
		#debugText = 'ID: %d, ' %(iCompany)
		# spread the company
		for i in range(len(cityValueList)):
			city = cityValueList[i][0]
			if city.isHasCorporation(iCompany):
				#debugText += '%s:%d(skip), ' %(city.getName(), cityValueList[i][1])
				continue
			if iMaxCompanies == 0:
				break
			if iCompanyCount >= iMaxCompanies and i >= iMaxCompanies: # don't spread to weak cities if the limit was reached
				#debugText += 'limit reached'
				break
			city.setHasCorporation(iCompany, True, True, True)
			#debugText += '%s(OK!), ' %(city.getName())
			break
		#print debugText
		
		# if the limit was exceeded, remove company from the worst city
		if iCompanyCount > iMaxCompanies:
			for i in range(len(cityValueList)-1, 0, -1):
				city = cityValueList[i][0]
				if city.isHasCorporation(iCompany):
					city.setHasCorporation(iCompany, False, True, True)
					break


	def onCityAcquired(self, argsList):
		iPreviousOwner, iNewOwner, city, bConquest, bTrade = argsList
		
		for iCompany in range(iNumCorporations):
			if city.isHasCorporation(iCompany):
				if self.getCityValue(city, iCompany) < 0:
					city.setHasCorporation(iCompany, False, True, True)


	def getCityValue(self, city, iCompany):
		if city is None: return -1
		elif city.isNone(): return -1
		
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
			if not iOwnerCiv in lTradingCompanyCivs:
				return -1
			if iOwnerCiv == iNetherlands:
				iValue += 2
		elif iCompany == iSilkRoute:
			if city.getRegionID() in [rCentralAsia, rPersia]:
				iValue += 2
			elif city.getRegionID() == rChina:
				iValue -= 2
		
		# geographical requirements
		tPlot = location(city)
		if iCompany == iSilkRoute:
			if tPlot in lMiddleEastExceptions:
				return -1
			if not self.isCityInArea(tPlot, tSilkRouteTL, tSilkRouteBR) and not self.isCityInArea(tPlot, tMiddleEastTL, tMiddleEastBR):
				return -1
		if iCompany == iTradingCompany:
			if not self.isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR) and not self.isCityInArea(tPlot, tSubSaharanAfricaTL, tSubSaharanAfricaBR) and not self.isCityInArea(tPlot, tSouthAsiaTL, tSouthAsiaBR) and not (city.isHasRealBuilding(iTradingCompanyBuilding) or city.isHasRealBuilding(iIberianTradingCompanyBuilding)):
				return -1
			elif self.isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR):
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
					
		if not bFound: return -1
		iValue += iTempValue
		
		# competition
		if iCompany == iCerealIndustry and city.isHasCorporation(iFishingIndustry): iValue /= 2
		elif iCompany == iFishingIndustry and city.isHasCorporation(iCerealIndustry): iValue /= 2
		elif iCompany == iSteelIndustry and city.isHasCorporation(iTextileIndustry): iValue /= 2
		elif iCompany == iTextileIndustry and city.isHasCorporation(iSteelIndustry): iValue /= 2
		elif iCompany == iOilIndustry and city.isHasCorporation(iComputerIndustry): iValue /= 2
		elif iCompany == iComputerIndustry and city.isHasCorporation(iOilIndustry): iValue /= 2
		
		# threshold
		if iValue < 4: return -1
		
		# spread it out
		iValue -= owner.countCorporations(iCompany)*2
		
		return iValue

	def isCityInArea(self, tCityPos, tTL, tBR):

		x, y = tCityPos
		tlx, tly = tTL
		brx, bry = tBR

		return ((x >= tlx) and (x <= brx) and (y >= tly) and (y <= bry))