# Rhye's and Fall of Civilization - Communications

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
import Popup
from Consts import *
from StoredData import *
import RFCUtils
utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

#scrambled pools
tPool1 = (iEgypt, -1, -1, -1, -1, -1,
	iChina, -1, -1, -1, -1, -1,
	iBabylonia, -1, -1, -1, -1, -1,
	iGreece, -1, -1, -1, -1, -1,
	iIndia, -1, -1, -1, -1, -1)

tPool2 = (iEgypt, -1, 
	iCarthage, -1,
	iChina, -1,
	iRome, -1,
	iBabylonia, iMaya,
	iGreece, -1,
	iIndia, iEthiopia,
	iJapan, -1,	    
	iPersia, -1)


tPool3 = (iEgypt,  
	iTurkey,
	iEngland,
	iInca,
	iCarthage,
	iRussia,
	iChina,
	iRome,	
	iVikings,
	iBabylonia,
	iAztecs,
	iEthiopia,
	iNetherlands,
	iItaly,
	iMongolia,
	iKhmer,
	iIndonesia,
	iSpain,
	iGreece,
	iMali,
	iMaya,
	iHolyRome,
	iIndia,
	iAmerica,
	iPortugal,	
	iJapan,
	iPersia,
	iFrance,
	iByzantium,
	iKorea,
	iMughals,
	iGermany,
	iThailand,
	iTamils,
	iPoland,
	iMoors,
	iCongo,
	iTibet,
	iBrazil,
	iArgentina,
	iCanada,
	iPolynesia,
	iHarappa)


class Communications:
       	
	def checkTurn(self, iGameTurn):
		#self.decay(iIndia) #debug
		#if (iGameTurn >= 25 and iGameTurn <= 95):
		if (iGameTurn >= getTurnForYear(-2250) and iGameTurn <= getTurnForYear(-680)):
			i = (iGameTurn + data.iSeed/10 - 5) % (len(tPool1))
			iCiv = tPool1[i]
##			#shuffle			
##			if (i % 2 == 0):
##				iCiv = i/2
##			else:
##				iCiv = iNumMajorPlayers/2 + i/2  
			if (iCiv >= 0 and iCiv < iNumMajorPlayers):
				if (gc.getPlayer(iCiv).isAlive() and iGameTurn >= getTurnForYear(tBirth[iCiv]+utils.getTurns(15))): # edead: RFCM
					if (not gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iElectricity)):
						self.decay(iCiv)
		#elif (iGameTurn > 95 and iGameTurn <= 168):
		elif (iGameTurn > getTurnForYear(-680) and iGameTurn <= getTurnForYear(410)): # edead: RFCM
			i = (iGameTurn + data.iSeed/10 - 5) % (len(tPool2))
			iCiv = tPool2[i]
  
			if (iCiv >= 0 and iCiv < iNumMajorPlayers):
				if (gc.getPlayer(iCiv).isAlive() and iGameTurn >= getTurnForYear(tBirth[iCiv]+utils.getTurns(15))): # edead: RFCM
					if (not gc.getTeam(gc.getPlayer(iCiv).getTeam()).isHasTech(iElectricity)):
						self.decay(iCiv)
		else:
			i = (iGameTurn + data.iSeed/10 - 5) % (len(tPool3))
			j = ((iGameTurn + data.iSeed/10 - 5)+13) % (len(tPool3))
			iCiv1 = tPool3[i]
			iCiv2 = tPool3[j]	  
			if (iCiv1 >= 0 and iCiv1 < iNumMajorPlayers):
				if (gc.getPlayer(iCiv1).isAlive() and iGameTurn >= getTurnForYear(tBirth[iCiv1]+utils.getTurns(15))): # edead: RFCM
					if (not gc.getTeam(gc.getPlayer(iCiv1).getTeam()).isHasTech(iElectricity)):
						self.decay(iCiv1)
			if (iCiv2 >= 0 and iCiv2 < iNumMajorPlayers):
				if (gc.getPlayer(iCiv2).isAlive() and iGameTurn >= getTurnForYear(tBirth[iCiv2]+utils.getTurns(15))): # edead: RFCM
					if (not gc.getTeam(gc.getPlayer(iCiv2).getTeam()).isHasTech(iElectricity)):
						self.decay(iCiv2)

			

	def decay(self, iCiv):

		teamCiv = gc.getTeam(gc.getPlayer(iCiv).getTeam())
		iCounter = 0
		
		# Initialize list
		lContacts = [i for i in range(iNumPlayers) if gc.getPlayer(i).isAlive() and teamCiv.canContact(i) and teamCiv.canCutContact(i)]
								
		# master/vassal relationships: if master can be seen, don't cut vassal contact and vice versa
		lRemove = []
		for iLoopPlayer in range(iNumPlayers):
			for iContact in lContacts:
				if gc.getTeam(iContact).isVassal(iLoopPlayer) and iLoopPlayer not in lContacts:
					lRemove.append(iContact)
				elif gc.getTeam(iLoopPlayer).isVassal(iContact) and iLoopPlayer not in lContacts:
					lRemove.append(iContact)
					
		# if there are still vassals in the list, their masters are too -> remove the vassals, and cut contact when their masters are chosen
		for iContact in lContacts:
			if gc.getTeam(iContact).isAVassal() and iContact not in lRemove:
				lRemove.append(iContact)
					
		for iLoopCiv in lRemove:
			if iLoopCiv in lContacts: lContacts.remove(iLoopCiv)
								
		# choose up to four random contacts to cut
		for i in range(4):
			if len(lContacts) == 0: break
			
			iContact = utils.getRandomEntry(lContacts)
			
			lOurCivs = [iCiv]
			lTheirCivs = [iContact]
			
			# remove contacts for all vassals on both sides as well
			for iLoopCiv in range(iNumPlayers):
				if gc.getTeam(iLoopCiv).isVassal(iCiv):
					lOurCivs.append(iLoopCiv)
				elif gc.getTeam(iLoopCiv).isVassal(iContact):
					lTheirCivs.append(iLoopCiv)
					
			for iOurCiv in lOurCivs:
				for iTheirCiv in lTheirCivs:
					#utils.debugTextPopup('Cut contact between ' + gc.getPlayer(iOurCiv).getCivilizationShortDescription(0) + ' and ' + gc.getPlayer(iTheirCiv).getCivilizationShortDescription(0))
					gc.getTeam(iOurCiv).cutContact(iTheirCiv)
					
			lContacts.remove(iContact)


	def onBuildingBuilt(self, iPlayer, iBuilding, city):
		return

	def onCityAcquired(self, city):
		return