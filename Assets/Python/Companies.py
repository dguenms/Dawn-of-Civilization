# The Sword of Islam - Companies

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Consts as con
from StoredData import sd
import RFCUtils
from operator import itemgetter

# globals
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

utils = RFCUtils.RFCUtils()

iNumPlayers = con.iNumPlayers
iNumTotalPlayers = con.iNumTotalPlayers
iNumCompanies = 9

(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iTextileIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry) = range(iNumCompanies)

tCompanyTechs = (con.iCurrency, con.iAstronomy, con.iBiology, con.iRefrigeration, con.iSteamPower, con.iSteel, con.iCombustion, con.iElectricity, con.iComputers)
tCompaniesLimit = (10, 12, 16, 10, 12, 12, 6, 10, 12) # kind of arbitrary currently, see how this plays out

lTradingCompanyCivs = [con.iSpain, con.iFrance, con.iEngland, con.iPortugal, con.iNetherlands, con.iVikings] # Vikings too now

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

		iCompany = iGameTurn % iNumCompanies
		self.checkCompany(iCompany, iGameTurn)

		iCompany = (iGameTurn + 4) % iNumCompanies
		self.checkCompany(iCompany, iGameTurn)


	def checkCompany(self, iCompany, iGameTurn):
		
		if (iCompany == iSilkRoute and iGameTurn > getTurnForYear(1500)) or (iCompany == iTradingCompany and iGameTurn > getTurnForYear(1800)) or (iCompany == iTextileIndustry and iGameTurn > getTurnForYear(1920)):
			iMaxCompanies = 0
		else:
			iMaxCompanies = tCompaniesLimit[iCompany]
		
		# loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
		cityValueList = []
		for iPlayer in range(iNumPlayers):
			if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(tCompanyTechs[iCompany]) and (gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(con.iCorporation) or iCompany <= iTradingCompany):
				apCityList = PyPlayer(iPlayer).getCityList()
				for pCity in apCityList:
					city = pCity.GetCy()
					iValue = self.getCityValue(city, iCompany)
					if iValue > 0: 
						cityValueList.append((city, iValue * 10 + gc.getGame().getSorenRandNum(10, 'random bonus')))
					elif city.isHasCorporation(iCompany): # quick check to remove companies
						city.setHasCorporation(iCompany, False, True, True)
		
		# sort cities from highest to lowest value
		cityValueList.sort(key=itemgetter(1), reverse=True)
		
		# count the number of companies
		iCompanyCount = 0
		for iLoopPlayer in range(iNumPlayers):
			if gc.getPlayer(iLoopPlayer).isAlive():
				iCompanyCount += gc.getPlayer(iLoopPlayer).countCorporations(iCompany)
		
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
		
		for iCompany in range(iNumCompanies):
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
		
		# State Property
		if owner.getCivics(3) == con.iCivicCentralPlanning:
			bOtherCorp = False
			for iLoopCorporation in range(iNumCompanies):
				if city.isHasCorporation(iLoopCorporation) and iLoopCorporation != iCompany:
					bOtherCorp = True
					break
			if bOtherCorp:
				return -1

		# Mercantilism increases likeliness for trading company
		if iCompany == iTradingCompany and owner.getCivics(3) == con.iCivicMercantilism:
			iValue += 2
			
		# Tribalism increases likeliness for silk route
		if iCompany == iSilkRoute and owner.getCivics(2) == con.iCivicTribalism:
			iValue += 2

		# Free Market increases likeliness for all companies
		if owner.getCivics(3) == con.iCivicFreeMarket:
			iValue += 1

		# civilization requirements
		if iCompany == iTradingCompany:
			if not owner.getID() in lTradingCompanyCivs:
				return -1
			if owner.getID() == con.iNetherlands:
				iValue += 2
		elif iCompany == iSilkRoute:
			if owner.getID() == con.iMongolia:
				iValue += 2
			elif owner.getID() == con.iChina:
				iValue -= 2
		
		# geographical requirements
		tPlot = (city.getX(), city.getY())
		if iCompany == iSilkRoute and not self.isCityInArea(tPlot, tSilkRouteTL, tSilkRouteBR) and not self.isCityInArea(tPlot, tMiddleEastTL, tMiddleEastBR):
			return -1
		if iCompany == iTradingCompany:
			if not self.isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR) and not self.isCityInArea(tPlot, tSubSaharanAfricaTL, tSubSaharanAfricaBR) and not self.isCityInArea(tPlot, tSouthAsiaTL, tSouthAsiaBR) and not (city.isHasRealBuilding(con.iTradingCompany) or city.isHasRealBuilding(con.iIberianTradingCompany)):
				return -1
			elif self.isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR):
				iValue += 1
		
		# trade companies and fishing industry - coastal cities only
		if iCompany == iTradingCompany or iCompany == iFishingIndustry:
			if not city.isCoastal(20):
				return -1

		# penalty for silk route if coastal (mitigatable by harbor)
		if iCompany == iSilkRoute:
			if city.isCoastal(20):
				iValue -= 1
		
		# religions
		if iCompany == iSilkRoute:
			if owner.getStateReligion() in [con.iProtestantism, con.iCatholicism, con.iOrthodoxy]:
				iValue -= 1
		
		# various bonuses
		if iCompany == iSilkRoute:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iMarket)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iGrocer)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iHarbor)): iValue += 1

		elif iCompany == iTradingCompany:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iHarbor)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iCustomHouse)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iBank)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iTradingCompany)): iValue += 2

		elif iCompany == iCerealIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iGranary)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iGrocer)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iSupermarket)): iValue += 1

		elif iCompany == iFishingIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iLighthouse)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iHarbor)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iSupermarket)): iValue += 1
			
		elif iCompany == iTextileIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iMarket)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iFactory)): iValue += 1

		elif iCompany == iSteelIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iCoalPlant)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iIndustrialPark)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iIronWorks)): iValue += 3

		elif iCompany == iOilIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iBank)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iIndustrialPark)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iStockExchange)): iValue += 3

		elif iCompany == iLuxuryIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iTheatre)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iBroadcastTower)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iNationalGallery)): iValue += 3

		elif iCompany == iComputerIndustry:
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iFactory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iLaboratory)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iUniversity)): iValue += 1
			if city.hasBuilding(utils.getUniqueBuilding(iOwner, con.iCERNResearchComplex)): iValue += 3

		# trade routes
		iValue += city.getTradeRoutes() - 1
		
		# resources
		iTempValue = 0
		bFound = False
		for i in range(6):
			iBonus = gc.getCorporationInfo(iCompany).getPrereqBonus(i)
			if iBonus > -1:
				if city.getNumBonuses(iBonus) > 0: bFound = True
				if iCompany in [iFishingIndustry, iCerealIndustry, iTextileIndustry]:
					iTempValue += city.getNumBonuses(iBonus)
				elif iCompany == iOilIndustry:
					iTempValue += city.getNumBonuses(iBonus) * 4
				elif iCompany == iSilkRoute:
					if iBonus == con.iSilk:
						iTempValue += city.getNumBonuses(iBonus) * 4
					else:
						iTempValue += city.getNumBonuses(iBonus) * 2
				else:
					iTempValue += city.getNumBonuses(iBonus) * 2
		
		# Brazilian UP: sugar counts as oil for Oil Industry
		if owner.getID() == con.iBrazil and iCompany == iOilIndustry:
			iValue += city.getNumBonuses(con.iSugar) * 3
			if city.getNumBonuses(con.iSugar) > 0: bFound = True
					
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