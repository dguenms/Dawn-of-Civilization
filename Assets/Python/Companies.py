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
iNumCompanies = 8

(iSilkRoute, iTradingCompany, iCerealIndustry, iFishingIndustry, iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry) = range(iNumCompanies)

tCompanyTechs = (con.iCurrency, con.iAstronomy, con.iBiology, con.iRefrigeration, con.iSteel, con.iCombustion, con.iIndustrialism, con.iComputers)
tCompaniesLimit = (10, 12, 20, 10, 20, 8, 10, 12) # kind of arbitrary currently, see how this plays out

lTradingCompanyCivs = [con.iSpain, con.iFrance, con.iEngland, con.iPortugal, con.iNetherlands]

tSilkRouteTL = (80, 46)
tSilkRouteBR = (103, 52)

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
		#if iGameTurn < getTurnForYear(tCompaniesBirth[iCompany]):
		#	return
		
		if (iCompany == iSilkRoute and iGameTurn > getTurnForYear(1500)) or (iCompany == iTradingCompany and iGameTurn > getTurnForYear(1800)):
			iMaxCompanies = 0
		else:
			iMaxCompanies = tCompaniesLimit[iCompany]
		
		# loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
		cityValueList = []
		for iPlayer in range(iNumPlayers):
			if gc.getTeam(gc.getPlayer(iPlayer).getTeam()).isHasTech(tCompanyTechs[iCompany]):
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
		
		# debugText = 'ID: %d, ' %(iCompany)
		# spread the company
		for i in range(len(cityValueList)):
			city = cityValueList[i][0]
			if city.isHasCorporation(iCompany):
				# debugText += '%s:%d(skip), ' %(city.getName(), cityValueList[i][1])
				continue
			if iCompanyCount >= iMaxCompanies and i >= iMaxCompanies: # don't spread to weak cities if the limit was reached
				# debugText += 'limit reached'
				break
			city.setHasCorporation(iCompany, True, True, True)
			# debugText += '%s(OK!), ' %(city.getName())
			break
		# utils.echo(debugText)
		
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
		
		iValue = 0
		
		owner = gc.getPlayer(city.getOwner())
		ownerTeam = gc.getTeam(owner.getTeam())
		
		# State Property
		if owner.getCivics(3) == 18:
			return -1

		# Mercantilism increases likeliness for trading company
		if iCompany == iTradingCompany and owner.getCivics(3) == 17:
			iValue += 2

		# Free Market increases likeliness for all companies
		if owner.getCivics(3) == 19:
			iValue += 1

		# civilization requirements
		if iCompany == iTradingCompany:
			if not owner.getID() in lTradingCompanyCivs:
				return -1
			if owner.getID() == con.iNetherlands:
				iValue += 2
		elif iCompany == iSilkRoute:
			if owner.getID() == con.iMongolia:
				iValue += 1
		
		# geographical requirements
		tPlot = (city.getX(), city.getY())
		if iCompany == iSilkRoute and not self.isCityInArea(tPlot, tSilkRouteTL, tSilkRouteBR) and not self.isCityInArea(tPlot, tMiddleEastTL, tMiddleEastBR):
			return -1
		if iCompany == iTradingCompany:
			if not self.isCityInArea(tPlot, tCaribbeanTL, tCaribbeanBR) and not self.isCityInArea(tPlot, tSubSaharanAfricaTL, tSubSaharanAfricaBR) and not self.isCityInArea(tPlot, tSouthAsiaTL, tSouthAsiaBR):
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
			if owner.getStateReligion() == con.iJudaism or owner.getStateReligion() == con.iChristianity:
				iValue -= 1
		
		# various bonuses
		if iCompany == iSilkRoute:
			if city.getNumRealBuilding(con.iMarket) > 0 or city.getNumRealBuilding(con.iRomanForum) > 0 or city.getNumRealBuilding(con.iPersianApothecary) > 0: iValue += 1
			if city.getNumRealBuilding(con.iGrocer) > 0: iValue += 1
			if city.getNumRealBuilding(con.iHarbor) > 0 or city.getNumRealBuilding(con.iCarthageCothon) > 0: iValue += 1

		elif iCompany == iTradingCompany:
			if city.getNumRealBuilding(con.iHarbor) > 0: iValue += 1
			if city.getNumRealBuilding(con.iCustomHouse) > 0 or city.getNumRealBuilding(con.iPortugalFeitoria) > 0: iValue += 1
			if city.getNumRealBuilding(con.iBank) > 0 or city.getNumRealBuilding(con.iEnglishStockExchange) > 0: iValue += 1

		elif iCompany == iCerealIndustry:
			if city.getNumRealBuilding(con.iGranary) > 0 or city.getNumRealBuilding(con.iIncanTerrace) > 0: iValue += 1
			if city.getNumRealBuilding(con.iGrocer) > 0: iValue += 1
			if city.getNumRealBuilding(con.iSupermarket) > 0 or city.getNumRealBuilding(con.iAmericanMall) > 0: iValue += 1

		elif iCompany == iFishingIndustry:
			if city.getNumRealBuilding(con.iLighthouse) > 0 or city.getNumRealBuilding(con.iVikingTradingPost) > 0: iValue += 1
			if city.getNumRealBuilding(con.iHarbor) > 0 or city.getNumRealBuilding(con.iCarthageCothon) > 0: iValue += 1
			if city.getNumRealBuilding(con.iSupermarket) > 0 or city.getNumRealBuilding(con.iAmericanMall) > 0: iValue += 1

		elif iCompany == iSteelIndustry:
			if city.getNumRealBuilding(con.iFactory) > 0 or city.getNumRealBuilding(con.iGermanAssemblyPlant) > 0: iValue += 1
			if city.getNumRealBuilding(con.iCoalPlant) > 0 or city.getNumRealBuilding(con.iJapaneseShalePlant) > 0: iValue += 1
			if city.getNumRealBuilding(con.iIndustrialPark) > 0: iValue += 1
			if city.getNumRealBuilding(con.iIronWorks) > 0: iValue += 3

		elif iCompany == iOilIndustry:
			if city.getNumRealBuilding(con.iBank) > 0 or city.getNumRealBuilding(con.iEnglishStockExchange) > 0: iValue += 1
			if city.getNumRealBuilding(con.iIndustrialPark) > 0: iValue += 1
			if city.getNumRealBuilding(con.iWallStreet) > 0: iValue += 3

		elif iCompany == iLuxuryIndustry:
			if city.getNumRealBuilding(con.iFactory) > 0 or city.getNumRealBuilding(con.iGermanAssemblyPlant) > 0: iValue += 1
			if city.getNumRealBuilding(con.iTheatre) > 0 or city.getNumRealBuilding(con.iFrenchSalon) > 0 or city.getNumRealBuilding(con.iByzantineHippodrome) > 0 or city.getNumRealBuilding(con.iChinesePavillion) > 0: iValue += 1
			if city.getNumRealBuilding(con.iBroadcastTower) > 0: iValue += 1
			if city.getNumRealBuilding(con.iHermitage) > 0: iValue += 3

		elif iCompany == iComputerIndustry:
			if city.getNumRealBuilding(con.iFactory) > 0 or city.getNumRealBuilding(con.iGermanAssemblyPlant) > 0: iValue += 1
			if city.getNumRealBuilding(con.iLaboratory) > 0 or city.getNumRealBuilding(con.iRussianResearchInstitute) > 0: iValue += 1
			if city.getNumRealBuilding(con.iUniversity) > 0 or city.getNumRealBuilding(con.iKoreanSeowon) > 0: iValue += 1
			if city.getNumRealBuilding(con.iChannelTunnel) > 0: iValue += 3

		# trade routes
		iValue += city.getTradeRoutes() - 1
		
		# resources
		iTempValue = 0
		bFound = False
		for i in range(4):
			iBonus = gc.getCorporationInfo(iCompany).getPrereqBonus(i)
			if iBonus > -1:
				if city.getNumBonuses(iBonus) > 0: bFound = True
				if iCompany in [iFishingIndustry, iCerealIndustry]:
					iTempValue += city.getNumBonuses(iBonus)
				elif iCompany == iOilIndustry:
					iTempValue += city.getNumBonuses(iBonus) * 4
				else:
					iTempValue += city.getNumBonuses(iBonus) * 2
		if not bFound: return -1
		iValue += iTempValue
		
		# competition
		if iCompany == iCerealIndustry and city.isHasCorporation(iFishingIndustry): iValue /= 2
		elif iCompany == iFishingIndustry and city.isHasCorporation(iCerealIndustry): iValue /= 2
		elif iCompany in [iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry]:
			lOtherCompanies = []
			for iTempCompany in [iSteelIndustry, iOilIndustry, iLuxuryIndustry, iComputerIndustry]:
				if iTempCompany != iCompany:
					lOtherCompanies.append(iTempCompany)
			iValue *= (4 - len(lOtherCompanies)) / 4
		
		# protection for already established companies (in case of removals)
		if city.isHasCorporation(iCompany):
			iValue += 1
		
		# threshold
		if iValue < 3: return -1
		
		# spread it out
		iValue -= owner.countCorporations(iCompany)
		
		return iValue

	def isCityInArea(self, tCityPos, tTL, tBR):

		x, y = tCityPos
		tlx, tly = tTL
		brx, bry = tBR

		if (x > tlx-1) and (x < brx+1) and (y > tly-1) and (y < bry+1):
			return True
		else:
			return False