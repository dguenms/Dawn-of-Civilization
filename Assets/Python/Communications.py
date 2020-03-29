# Rhye's and Fall of Civilization - Communications

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
import Popup
from Consts import *
from StoredData import *
from RFCUtils import *

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

#scrambled pools
tPool1 = (iCivEgypt, NoCiv, NoCiv, NoCiv, NoCiv, NoCiv,
	iCivChina, NoCiv, NoCiv, NoCiv, NoCiv, NoCiv,
	iCivBabylonia, NoCiv, NoCiv, NoCiv, NoCiv, NoCiv,
	iCivGreece, NoCiv, NoCiv, NoCiv, NoCiv, NoCiv,
	iCivIndia, NoCiv, NoCiv, NoCiv, NoCiv, NoCiv)

tPool2 = (iCivEgypt, NoCiv, 
	iCivCarthage, NoCiv,
	iCivChina, NoCiv,
	iCivRome, NoCiv,
	iCivBabylonia, iCivMaya,
	iCivGreece, NoCiv,
	iCivIndia, iCivEthiopia,
	iCivJapan, NoCiv,	    
	iCivPersia, NoCiv)


tPool3 = (iCivEgypt,  
	iCivOttomans,
	iCivEngland,
	iCivInca,
	iCivCarthage,
	iCivRussia,
	iCivChina,
	iCivRome,	
	iCivVikings,
	iCivTurks,
	iCivBabylonia,
	iCivAztecs,
	iCivEthiopia,
	iCivNetherlands,
	iCivItaly,
	iCivMongols,
	iCivKhmer,
	iCivIndonesia,
	iCivSpain,
	iCivGreece,
	iCivMali,
	iCivMaya,
	iCivHolyRome,
	iCivIndia,
	iCivAmerica,
	iCivPortugal,	
	iCivJapan,
	iCivPersia,
	iCivFrance,
	iCivByzantium,
	iCivKorea,
	iCivMughals,
	iCivGermany,
	iCivThailand,
	iCivTamils,
	iCivPoland,
	iCivMoors,
	iCivCongo,
	iCivTibet,
	iCivBrazil,
	iCivArgentina,
	iCivCanada,
	iCivPolynesia,
	iCivHarappa)


class Communications:

	def checkTurn(self, iGameTurn):
		if year().between(-2250, -680):
			i = (iGameTurn + data.iSeed/10 - 5) % len(tPool1)
			iCiv = tPool1[i]
			self.canDecay(iGameTurn, iCiv)
		elif year().between(-680, 410): # edead: RFCM
			i = (iGameTurn + data.iSeed/10 - 5) % len(tPool2)
			iCiv = tPool2[i]
			self.canDecay(iGameTurn, iCiv)
		else:
			i = (iGameTurn + data.iSeed/10 - 5) % len(tPool3)
			j = ((iGameTurn + data.iSeed/10 - 5)+13) % len(tPool3)
			iCiv1 = tPool3[i]
			iCiv2 = tPool3[j]
			self.canDecay(iGameTurn, iCiv1)
			self.canDecay(iGameTurn, iCiv2)

	def canDecay(self, iGameTurn, iCiv):
		if player(iCiv).isAlive() and not is_minor(iCiv):
			if iGameTurn >= year(dBirth[iCiv]) + turns(15): # edead: RFCM
				if not team(iCiv).isHasTech(iElectricity):
					self.decay(slot(iCiv))

	def decay(self, iPlayer):
		contacts = players.major().alive().where(lambda p: team(iPlayer).canContact(p) and team(iPlayer).canCutContact(p))
		
		# master/vassal relationships: keep only masters where contact can be cut with all vassals
		dVassals = vassals()
		contacts = contacts.where(lambda p: all(iVassal in contacts for iVassal in dVassals[p]))
		
		# remove all vassals, vassals where the master contact cannot be cut need to be removed -> other vassals contact will be cut along with their masters
		contacts = contacts.where(lambda p: not team(p).isAVassal())
		
		# choose up to four random contacts to cut
		for iContact in contacts.sample(4):
			ours = players.vassals(iPlayer).including(iPlayer)
			theirs = players.vassals(iContact).including(iContact)
			
			for iTheirPlayer, iOurPlayer in permutations(theirs, ours):
				team(iOurPlayer).cutContact(iTheirPlayer)


	def onBuildingBuilt(self, iPlayer, iBuilding, city):
		return

	def onCityAcquired(self, city):
		return