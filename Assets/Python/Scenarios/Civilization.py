from Core import *


class Civilization(object):

	def __init__(self, iCiv, iLeader=None, iGold=None, iStateReligion=None, lCivics=[]):
		self.iCiv = iCiv
	
		self.iLeader = iLeader
		self.iGold = iGold
		self.iStateReligion = iStateReligion
		self.lCivics = lCivics
	
	@property
	def player(self):
		return player(self.iCiv)
	
	def apply(self):
		if self.iLeader is not None:
			self.player.setLeader(self.iLeader)
		
		if self.iGold is not None:
			self.player.setGold(self.iGold)
		
		if self.iStateReligion is not None:
			self.player.setLastStateReligion(self.iStateReligion)
		
		for iCivic in self.lCivics:
			self.player.setCivics(infos.civic(iCivic).getCivicOptionType(), iCivic)
	
	
