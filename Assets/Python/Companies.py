# The Sword of Islam - Companies

from CvPythonExtensions import *
import CvUtil
import PyHelpers
from Consts import *
from RFCUtils import utils
from operator import itemgetter

# globals
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

tCompanyTechs = (iCurrency, iExploration, iBiology, iRefrigeration, iThermodynamics, iMetallurgy, iRefining, iConsumerism, iComputers)
tCompaniesLimit = (10, 12, 16, 10, 12, 12, 6, 10, 12) # kind of arbitrary currently, see how this plays out

lTradingCompanyCivs = [iSpain, iFrance, iEngland, iPortugal, iNetherlands, iVikings] # Vikings too now

tSilkRouteTL = (80, 46)
tSilkRouteBR = (99, 52)

tMiddleEastTL = (68, 38)
tMiddleEastBR = (85, 46)

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
		
		if (iCompany == iSilkRoute and iGameTurn > getTurnForYear(1500)) or (iCompany == iTradingCompany and iGameTurn > getTurnForYear(1800)) or (iCompany == iTextileIndustry and iGameTurn > getTurnForYear(1920)):
			iMaxCompanies = 0
		else:
			iMaxCompanies = tCompaniesLimit[iCompany]
		
		# count the number of companies
		iCompanyCount = 0
		for iLoopPlayer in range(iNumPlayers):
			if gc.getPlayer(iLoopPlayer).isAlive():
				iCompanyCount += gc.getPlayer(iLoopPlayer).countCorporations(iCompany)
		
		# return if gameturn is beyond company fall date and removed from all cities
		if iMaxCompanies == 0 and iCompanyCount == 0:
			return
		
		# loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
		cityValueList = []
		for iPlayer in range(iNumPlayers):
			if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(tCompanyTechs[iCompany]) and (gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(iEconomics) or iCompany <= iTradingCompany):
				for city in utils.getCityList(iPlayer):
					iValue = self.getCityValue(city, iCompany)
					if iValue > 0: 
						cityValueList.append((city, iValue * 10 + gc.getGame().getSorenRandNum(10, 'random bonus')))
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
		owner = gc.getPlayer(iOwner)
		ownerTeam = gc.getTeam(owner.getTeam())
		
		# Central Planning: only one company per city
		if owner.getCivics(iCivicsEconomy) == iCentralPlanning:
			for iLoopCorporation in range(iNumCorporations):
				if city.isHasCorporation(iLoopCorporation) and iLoopCorporation != iCompany:
					return -1

		# Colonialism increases likeliness for trading company
		if iCompany == iTradingCompany and owner.getCivics(iCivicsTerritory) == iColonialism:
			iValue += 2
			
		# Merchant Trade increases likeliness for silk route
		if iCompany == iSilkRoute and owner.getCivics(iCivicsEconomy) == iMerchantTrade:
			iValue += 2

		# Free Enterprise increases likeliness for all companies
		if owner.getCivics(iCivicsEconomy) == iFreeEnterprise:
			iValue += 1

		# civilization requirements
		if iCompany == iTradingCompany:
			if not iOwner in lTradingCompanyCivs:
				return -1
			if iOwner == iNetherlands:
				iValue += 2
		elif iCompany == iSilkRoute:
			if city.getRegionID() in [rCentralAsia, rPersia]:
				iValue += 2
			elif city.getRegionID() == rChina:
				iValue -= 2
		
		# geographical requirements
		tPlot = (city.getX(), city.getY())
		if iCompany == iSilkRoute and not self.isCityInArea(tPlot, tSilkRouteTL, tSilkRouteBR) and not self.isCityInArea(tPlot, tMiddleEastTL, tMiddleEastBR):
			return -1
		if iCompany == iTradingCompany:
			if not self.isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR) and not self.isCityInArea(tPlot, tSubSaharanAfricaTL, tSubSaharanAfricaBR) and not self.isCityInArea(tPlot, tSouthAsiaTL, tSouthAsiaBR) and not (city.isHasRealBuilding(iTradingCompany) or city.isHasRealBuilding(iIberianTradingCompany)):
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
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iWeaver)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iMarket)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iStable)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iHarbor)): iValue += 1

		elif iCompany == iTradingCompany:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iHarbor)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iCustomsHouse)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iBank)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iTradingCompany)): iValue += 2

		elif iCompany == iCerealIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iGranary)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iSewer)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iSupermarket)): iValue += 1

		elif iCompany == iFishingIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iLighthouse)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iHarbor)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iSupermarket)): iValue += 1
			
		elif iCompany == iTextileIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iMarket)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iWeaver)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iFactory)): iValue += 1

		elif iCompany == iSteelIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iCoalPlant)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iIndustrialPark)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iIronworks)): iValue += 3

		elif iCompany == iOilIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iBank)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iDistillery)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iIndustrialPark)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iStockExchange)): iValue += 3

		elif iCompany == iLuxuryIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iWeaver)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iDepartmentStore)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iNationalGallery)): iValue += 3

		elif iCompany == iComputerIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iLaboratory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iUniversity)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, iCERN)): iValue += 3

		# trade routes
		iValue += city.getTradeRoutes() - 1
		
		# resources
		iTempValue = 0
		bFound = False
		for i in range(6):
			iBonus = gc.getCorporationInfo(iCompany).getPrereqBonus(i)
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
		if iOwner == iBrazil and iCompany == iOilIndustry:
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
		#elif iCompany in [iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry]:
		#	lOtherCompanies = []
		#	for iTempCompany in [iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry]:
		#		if iTempCompany != iCompany and city.isHasCorporation(iTempCompany):
		#			lOtherCompanies.append(iTempCompany)
		#	iValue *= (4 - len(lOtherCompanies))
		#	iValue /= 4
		
		# protection for already established companies (in case of removals)
		#if city.isHasCorporation(iCompany):
		#	iValue += 1
		
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