from Civics import *
from unittest import *


class TestCivics(TestCase):

	def test_initial_values(self):
		gc.getPlayer(0).setCivics(iCivicsGovernment, iDemocracy)
		gc.getPlayer(0).setCivics(iCivicsLegitimacy, iConstitution)
		gc.getPlayer(0).setCivics(iCivicsSociety, iEgalitarianism)
		gc.getPlayer(0).setCivics(iCivicsEconomy, iPublicWelfare)
		gc.getPlayer(0).setCivics(iCivicsReligion, iSecularism)
		gc.getPlayer(0).setCivics(iCivicsTerritory, iMultilateralism)
		
		civics = Civics.player(0)
		
		try:
			self.assertEqual(civics.iGovernment, iDemocracy)
			self.assertEqual(civics.iLegitimacy, iConstitution)
			self.assertEqual(civics.iSociety, iEgalitarianism)
			self.assertEqual(civics.iEconomy, iPublicWelfare)
			self.assertEqual(civics.iReligion, iSecularism)
			self.assertEqual(civics.iTerritory, iMultilateralism)
		finally:
			gc.getPlayer(0).setCivics(iCivicsGovernment, iMonarchy)
			gc.getPlayer(0).setCivics(iCivicsLegitimacy, iAuthority)
			gc.getPlayer(0).setCivics(iCivicsSociety, iTraditionalism)
			gc.getPlayer(0).setCivics(iCivicsEconomy, iRedistribution)
			gc.getPlayer(0).setCivics(iCivicsReligion, iDeification)
			gc.getPlayer(0).setCivics(iCivicsTerritory, iSovereignty)
	
	def test_active(self):
		gc.getPlayer(0).setCivics(iCivicsGovernment, iDemocracy)
		
		civics = Civics.player(0)
		
		try:
			self.assertEqual(civics.active(iDemocracy), True)
			self.assertEqual(civics.active(iMonarchy), False)
			self.assertEqual(civics.active(iSovereignty), True)
			self.assertEqual(civics.active(iMultilateralism), False)
		finally:
			gc.getPlayer(0).setCivics(iCivicsGovernment, iMonarchy)
	
	def test_contains_single(self):
		gc.getPlayer(0).setCivics(iCivicsGovernment, iDemocracy)
		
		civics = Civics.player(0)
		
		try:
			self.assertEqual(iDemocracy in civics, True)
			self.assertEqual(iMonarchy in civics, False)
			self.assertEqual(iSovereignty in civics, True)
			self.assertEqual(iMultilateralism in civics, False)
		finally:
			gc.getPlayer(0).setCivics(iCivicsGovernment, iMonarchy)
	
	def test_contains_any(self):
		gc.getPlayer(0).setCivics(iCivicsGovernment, iDemocracy)
		
		civics = Civics.player(0)
		
		try:
			self.assertEqual((iMonarchy, iDemocracy) in civics, True)
			self.assertEqual((iMonarchy, iRepublic) in civics, False)
			self.assertEqual((iRepublic, iDemocracy) in civics, True)
			self.assertEqual((iSovereignty, iDemocracy) in civics, True)
		finally:
			gc.getPlayer(0).setCivics(iCivicsGovernment, iMonarchy)
	
	def test_contains_all(self):
		gc.getPlayer(0).setCivics(iCivicsGovernment, iDemocracy)
		gc.getPlayer(0).setCivics(iCivicsEconomy, iPublicWelfare)
		
		civics = Civics.player(0)
		
		try:
			self.assertEqual((iDemocracy, iPublicWelfare) in civics, True)
			self.assertEqual((iMonarchy, iPublicWelfare) in civics, False)
			self.assertEqual((iDemocracy, iRedistribution) in civics, False)
			self.assertEqual((iDemocracy, iSovereignty) in civics, True)
		finally:
			gc.getPlayer(0).setCivics(iCivicsGovernment, iMonarchy)
			gc.getPlayer(0).setCivics(iCivicsEconomy, iRedistribution)
	
	def test_contain_combined(self):
		gc.getPlayer(0).setCivics(iCivicsGovernment, iDemocracy)
		gc.getPlayer(0).setCivics(iCivicsEconomy, iPublicWelfare)
		
		civics = Civics.player(0)
		
		try:
			self.assertEqual((iDemocracy, iPublicWelfare) in civics, True)
			self.assertEqual((iMonarchy, iDemocracy, iPublicWelfare) in civics, True)
			self.assertEqual((iMonarchy, iPublicWelfare) in civics, False)
			self.assertEqual((iMonarchy, iDemocracy, iFreeEnterprise, iPublicWelfare) in civics, True)
			self.assertEqual((iDemocracy, iFreeEnterprise) in civics, False)
		finally:
			gc.getPlayer(0).setCivics(iCivicsGovernment, iMonarchy)
			gc.getPlayer(0).setCivics(iCivicsEconomy, iRedistribution)
	
	def test_not_contain(self):
		gc.getPlayer(0).setCivics(iCivicsGovernment, iDemocracy)
		
		civics = Civics.player(0)
		
		try:
			self.assertEqual(iDemocracy not in civics, False)
			self.assertEqual(iMonarchy not in civics, True)
			self.assertEqual((iMonarchy, iRepublic) not in civics, True)
			self.assertEqual((iMonarchy, iDemocracy) not in civics, False)
		finally:
			gc.getPlayer(0).setCivics(iCivicsGovernment, iMonarchy)
	
	def test_of(self):
		civics = Civics.of(iDemocracy, iConstitution)
		
		self.assertEqual(iDemocracy in civics, True)
		self.assertEqual(iConstitution in civics, True)
		self.assertEqual(iSovereignty in civics, False)
		self.assertEqual((iDemocracy, iConstitution) in civics, True)
		self.assertEqual((iMonarchy, iDemocracy) in civics, True)
		self.assertEqual((iCitizenship, iConstitution) in civics, True)
		self.assertEqual(iSovereignty not in civics, True)
		self.assertEqual(iMonarchy not in civics, True)
		self.assertEqual(iDemocracy not in civics, False)
	
	def test_notcivics_single(self):
		civics = notcivics(iDemocracy)
		
		self.assertEqual(civics, (iChiefdom, iDespotism, iMonarchy, iRepublic, iElective, iStateParty))
	
	def test_notcivics_multiple(self):
		civics = notcivics(iDespotism, iMonarchy, iRepublic)
		
		self.assertEqual(civics, (iChiefdom, iElective, iStateParty, iDemocracy))
		

test_cases = [
	TestCivics,
]
		
suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)