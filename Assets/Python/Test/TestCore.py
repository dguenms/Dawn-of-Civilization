from Core import *
from unittest import *

from TestUtils import setup

import types


def assertType(test, obj, expected_type):
	test.assertEqual(type(obj), expected_type)


class TestTurn(TestCase):

	def test_equals(self):
		self.assertEqual(Turn(10), Turn(10))

	def test_equals_int(self):
		self.assertEqual(Turn(10), 10)
		
	def test_add_turns(self):
		# given
		turn = Turn(10)
		
		# when
		added_turn = turn + Turn(10)
		
		# then
		self.assert_(isinstance(added_turn, Turn))
		self.assertEqual(added_turn, Turn(20))
		
	def test_add_int_to_turn(self):
		# given
		turn = Turn(10)
		
		# when
		added_turn = turn + 10
		
		# then
		self.assert_(isinstance(added_turn, Turn))
		self.assertEqual(added_turn, Turn(20))
		
	def test_subtract_turns(self):
		# given
		turn = Turn(20)
		
		# when
		subtracted_turn = turn - Turn(10)
		
		# then
		self.assert_(isinstance(subtracted_turn, Turn))
		self.assertEqual(subtracted_turn, Turn(10))
		
	def test_between(self):
		# given
		start = -3000
		end = -2000
		turn = Turn(2)
		
		# when/then
		self.assert_(turn.between(start, end))
		
	def test_not_between(self):
		# given
		start = -3000
		end = -2000
		turn = Turn(100)
		
		# when/then
		self.assert_(not turn.between(start, end))
		
	def test_between_at_border(self):
		# given
		start = -3000
		end = -2000
		turn = Turn(0) # 3000 BC
		
		# when/then
		self.assert_(turn.between(start, end))
		
	def test_between_inverse(self):
		# given
		start = -2000
		end = -3000
		turn = Turn(2)
		
		# when/then
		self.assert_(not turn.between(start, end))
		
	def test_deviate(self):
		# given
		turn = Turn(100)
		
		# when
		bExceeded = False
		for _ in range(1000):
			if not (90 <= turn.deviate(10) <= 110):
				bExceeded = True
				
		# then
		self.assert_(not bExceeded)
		
	def test_deviate_seed(self):
		# given
		turn = Turn(100)
		iSeed = 25
		
		# when
		new_turn = turn.deviate(10, 25)
		
		# then
		self.assertEqual(new_turn, 95)
		
		
class TestInfos(TestCase):

	def setUp(self):
		self.infos = Infos()
		
	def test_type(self):
		# given
		string = 'CIVILIZATION_EGYPT'
		expected_type = iEgypt
		
		# when
		actual_type = self.infos.type(string)
		
		# then
		self.assert_(isinstance(actual_type, int))
		self.assertEqual(actual_type, expected_type)
		
	def test_nonexistent_type(self):
		self.assertRaises(ValueError, self.infos.type, 'ABCDEF')
		
	def test_constant(self):
		# given
		string = 'CIV4_VERSION'
		expected_value = 319
		
		# when
		actual_value = self.infos.constant(string)
		
		# then
		self.assert_(isinstance(actual_value, int))
		self.assertEqual(actual_value, expected_value)
		
	def test_civ(self):
		# given
		iCiv = 0
		expected_civinfo = gc.getCivilizationInfo(iCiv)
		
		# when
		actual_civinfo = self.infos.civ(iCiv)
	
		# then
		self.assert_(isinstance(actual_civinfo, CvCivilizationInfo))
		self.assertEqual(actual_civinfo.getText(), expected_civinfo.getText())
		
	def test_civ_player(self):
		# given
		player = gc.getPlayer(0)
		expected_civinfo = gc.getCivilizationInfo(iEgypt)
		
		# when
		actual_civinfo = self.infos.civ(player)
		
		# then
		self.assert_(isinstance(actual_civinfo, CvCivilizationInfo))
		self.assertEqual(actual_civinfo.getText(), expected_civinfo.getText())
		
	def test_religion(self):
		# given
		iReligion = 0
		expected_religioninfo = gc.getReligionInfo(iReligion)
		
		# when
		actual_religioninfo = self.infos.religion(iReligion)
		
		# then
		self.assert_(isinstance(actual_religioninfo, CvReligionInfo))
		self.assertEqual(actual_religioninfo.getText(), expected_religioninfo.getText())
	
	def test_pagan_religion(self):
		# given
		iPaganReligion = 0
		expected_paganreligioninfo = gc.getPaganReligionInfo(iPaganReligion)
		
		# when
		actual_paganreligioninfo = self.infos.paganReligion(iPaganReligion)
		
		# then
		self.assert_(isinstance(actual_paganreligioninfo, CvInfoBase))
		self.assertEqual(actual_paganreligioninfo.getText(), expected_paganreligioninfo.getText())
	
	def test_pagan_religion_civ(self):
		# given
		iCiv = iBabylonia
		iExpectedPaganReligion = gc.getCivilizationInfo(iCiv).getPaganReligion()
		expected_paganreligioninfo = gc.getPaganReligionInfo(iExpectedPaganReligion)
		
		# when
		actual_paganreligioninfo = self.infos.paganReligion(iCiv)
		
		# then
		self.assert_(isinstance(actual_paganreligioninfo, CvInfoBase))
		self.assertEqual(actual_paganreligioninfo.getText(), expected_paganreligioninfo.getText())
		
	def test_gameSpeed(self):
		# given
		iGameSpeed = 0
		expected_gamespeedinfo = gc.getGameSpeedInfo(iGameSpeed)
		
		# when
		actual_gamespeedinfo = self.infos.gameSpeed(iGameSpeed)
		
		# then
		self.assert_(isinstance(actual_gamespeedinfo, CvGameSpeedInfo))
		self.assertEqual(actual_gamespeedinfo.getText(), expected_gamespeedinfo.getText())
		
	def test_gameSpeed_inferred(self):
		# given
		expected_gamespeedinfo = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType())
		
		# then
		actual_gamespeedinfo = self.infos.gameSpeed()
		
		# then
		self.assert_(isinstance(actual_gamespeedinfo, CvGameSpeedInfo))
		self.assertEqual(actual_gamespeedinfo.getText(), expected_gamespeedinfo.getText())
		
	def test_unit(self):
		# given
		iUnit = iSettler
		expected_unitinfo = gc.getUnitInfo(iSettler)
		
		# when
		actual_unitinfo = self.infos.unit(iUnit)
		
		# then
		self.assert_(isinstance(actual_unitinfo, CvUnitInfo))
		self.assertEqual(actual_unitinfo.getText(), expected_unitinfo.getText())
		
	def test_unit_instance(self):
		# given
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		expected_unitinfo = gc.getUnitInfo(4)
		
		# when
		actual_unitinfo = self.infos.unit(unit)
		
		# then
		try:
			self.assert_(isinstance(actual_unitinfo, CvUnitInfo))
			self.assertEqual(actual_unitinfo.getText(), expected_unitinfo.getText())
		
		# cleanup
		finally:
			unit.kill(False, 0)
		
	def test_unit_invalid(self):
		self.assertRaises(TypeError, self.infos.unit, gc.getMap().plot(0, 0))
		
	def test_feature(self):
		# given
		iFeature = iRainforest
		expected_featureinfo = gc.getFeatureInfo(iRainforest)
		
		# when
		actual_featureinfo = self.infos.feature(iFeature)
		
		# then
		self.assert_(isinstance(actual_featureinfo, CvFeatureInfo))
		self.assertEqual(actual_featureinfo.getText(), expected_featureinfo.getText())
		
	def test_feature_plot(self):
		# given
		plot = gc.getMap().plot(0, 0)
		plot.setFeatureType(iRainforest, 0)
		expected_featureinfo = gc.getFeatureInfo(iRainforest)
		
		# when
		actual_featureinfo = self.infos.feature(plot)
		
		# then
		try:
			self.assert_(isinstance(actual_featureinfo, CvFeatureInfo))
		
		# cleanup
		finally:
			plot.setFeatureType(-1, -1)
		
	def test_feature_invalid(self):
		self.assertRaises(TypeError, self.infos.feature, gc.getMap())
		
	def test_tech(self):
		# given
		iTech = 0
		expected_techinfo = gc.getTechInfo(0)
		
		# when
		actual_techinfo = self.infos.tech(iTech)
		
		# then
		self.assert_(isinstance(actual_techinfo, CvTechInfo))
		self.assertEqual(actual_techinfo.getText(), expected_techinfo.getText())
		
	def test_bonus(self):
		# given
		iBonus = 0
		expected_bonusinfo = gc.getBonusInfo(0)
		
		# when
		actual_bonusinfo = self.infos.bonus(iBonus)
		
		# then
		self.assert_(isinstance(actual_bonusinfo, CvBonusInfo))
		self.assertEqual(actual_bonusinfo.getText(), expected_bonusinfo.getText())
		
	def test_bonus_plot(self):
		# given
		plot = gc.getMap().plot(0, 0)
		plot.setBonusType(iIron)
		expected_bonusinfo = gc.getBonusInfo(iIron)
		
		# when
		actual_bonusinfo = self.infos.bonus(plot)
		
		# then
		try:
			self.assert_(isinstance(actual_bonusinfo, CvBonusInfo))
			self.assertEqual(actual_bonusinfo.getText(), expected_bonusinfo.getText())
		
		# cleanup
		finally:
			plot.setBonusType(-1)
		
	def test_bonus_invalid(self):
		self.assertRaises(TypeError, self.infos.bonus, gc.getMap())
		
	def test_handicap(self):
		# given
		expected_handicapinfo = gc.getHandicapInfo(gc.getGame().getHandicapType())
		
		# when
		actual_handicapinfo = self.infos.handicap()
		
		# then
		self.assert_(isinstance(actual_handicapinfo, CvHandicapInfo))
		self.assertEqual(actual_handicapinfo.getText(), expected_handicapinfo.getText())
		
	def test_corporation(self):
		# given
		iCorporation = 0
		expected_corporationinfo = gc.getCorporationInfo(0)
		
		# when
		actual_corporationinfo = self.infos.corporation(iCorporation)
		
		# then
		self.assert_(isinstance(actual_corporationinfo, CvCorporationInfo))
		self.assertEqual(actual_corporationinfo.getText(), expected_corporationinfo.getText())
		
	def test_building(self):
		# given
		iBuilding = 0
		expected_buildinginfo = gc.getBuildingInfo(0)
		
		# when
		actual_buildinginfo = self.infos.building(iBuilding)
		
		# then
		self.assert_(isinstance(actual_buildinginfo, CvBuildingInfo))
		self.assertEqual(actual_buildinginfo.getText(), expected_buildinginfo.getText())
		
	def test_art(self):
		# given
		string = 'INTERFACE_EVENT_BULLET'
		expected_path = ',Art/Interface/Buttons/Process/Blank.dds,Art/Interface/Buttons/Beyond_the_Sword_Atlas.dds,8,5'
		
		# when
		actual_path = self.infos.art(string)
		
		# then
		self.assertEqual(actual_path, expected_path)
		
	def test_art_nonexistent(self):
		self.assertRaises(ValueError, self.infos.art, 'ABCDEF')
		
	def test_commerce(self):
		# given
		iCommerce = 0
		expected_commerceinfo = gc.getCommerceInfo(0)
		
		# when
		actual_commerceinfo = self.infos.commerce(iCommerce)
		
		# then
		self.assert_(isinstance(actual_commerceinfo, CvCommerceInfo))
		self.assertEqual(actual_commerceinfo.getText(), expected_commerceinfo.getText())
		
	def test_promotions(self):
		promotions = self.infos.promotions()
	
		assertType(self, promotions, InfoCollection)
		self.assertEqual(len(promotions), gc.getNumPromotionInfos())
		
		for i, info in enumerate(promotions):
			self.assertEqual(i, info)
		
	def test_promotion(self):
		# given
		iPromotion = 0
		expected_promotioninfo = gc.getPromotionInfo(0)
		
		# when
		actual_promotioninfo = self.infos.promotion(iPromotion)
		
		# then
		self.assert_(isinstance(actual_promotioninfo, CvPromotionInfo))
		self.assertEqual(actual_promotioninfo.getText(), expected_promotioninfo.getText())
	
	def test_project(self):
		# given
		iProject = 0
		expected_projectinfo = gc.getProjectInfo(0)
		
		# when
		actual_projectinfo = self.infos.project(iProject)
		
		# then
		self.assert_(isinstance(actual_projectinfo, CvProjectInfo))
		self.assertEqual(actual_projectinfo.getText(), expected_projectinfo.getText())
	
	def test_leader(self):
		# given
		iLeader = 0
		expected_leaderheadinfo = gc.getLeaderHeadInfo(0)
		
		# when
		actual_leaderheadinfo = self.infos.leader(iLeader)
		
		# then
		self.assert_(isinstance(actual_leaderheadinfo, CvLeaderHeadInfo))
		self.assertEqual(actual_leaderheadinfo.getText(), expected_leaderheadinfo.getText())
	
	def test_leader_player(self):
		# given
		player = gc.getPlayer(0)
		expected_leaderheadinfo = gc.getLeaderHeadInfo(iRamesses)
		
		# then
		actual_leaderheadinfo = self.infos.leader(player)
		
		# then
		self.assert_(isinstance(actual_leaderheadinfo, CvLeaderHeadInfo))
		self.assertEqual(actual_leaderheadinfo.getText(), expected_leaderheadinfo.getText())
	
	def test_leader_invalid(self):
		self.assertRaises(TypeError, self.infos.leader, gc.getMap())
	
	def test_improvement(self):
		# given
		iImprovement = 0
		expected_improvementinfo = gc.getImprovementInfo(0)
		
		# when
		actual_improvementinfo = self.infos.improvement(iImprovement)
		
		# then
		self.assert_(isinstance(actual_improvementinfo, CvImprovementInfo))
		self.assertEqual(actual_improvementinfo.getText(), expected_improvementinfo.getText())
	
	def test_buildingClass(self):
		# given
		iBuildingClass = 0
		expected_buildingclassinfo = gc.getBuildingClassInfo(0)
		
		# when
		actual_buildingclassinfo = self.infos.buildingClass(iBuildingClass)
		
		# then
		self.assert_(isinstance(actual_buildingclassinfo, CvBuildingClassInfo))
		self.assertEqual(actual_buildingclassinfo.getText(), expected_buildingclassinfo.getText())
	
	def test_cultureLevel(self):
		# given
		iCultureLevel = 0
		expected_culturelevelinfo = gc.getCultureLevelInfo(0)
		
		# when
		actual_culturelevelinfo = self.infos.cultureLevel(iCultureLevel)
		
		# then
		self.assert_(isinstance(actual_culturelevelinfo, CvCultureLevelInfo))
		self.assertEqual(actual_culturelevelinfo.getText(), expected_culturelevelinfo.getText())
	
	def test_era(self):
		# given
		iEra = 0
		expected_erainfo = gc.getEraInfo(0)
		
		# when
		actual_erainfo = self.infos.era(iEra)
		
		# then
		self.assert_(isinstance(actual_erainfo, CvEraInfo))
		self.assertEqual(actual_erainfo.getText(), expected_erainfo.getText())
		
		
class TestDefaultDict(TestCase):

	def setUp(self):
		self.normaldict = {1: 'one', 2: 'two', 3: 'three'}
		self.defaultdict = DefaultDict(self.normaldict, 'other')
	
	def test_equals_dict(self):
		self.assertEqual(self.normaldict, self.defaultdict)
		
	def test_immutable_under_base_dictionary(self):
		self.normaldict[4] = 'four'
		
		self.assert_(4 not in self.defaultdict)
		
	def test_does_not_contain_missing(self):
		self.assert_(4 not in self.defaultdict)
		
	def test_returns_default_if_missing(self):
		self.assertEqual(self.defaultdict[4], 'other')
		
	def test_can_append_to_default_list(self):
		# given
		defaultdict = DefaultDict({1: ['one'], 2: ['two']}, [])
		
		# when
		defaultdict[3].append('three')
		
		# then
		self.assertEqual(defaultdict[3], ['three'])
		
	def test_defaultdict(self):
		test_dict = defaultdict(self.normaldict, 0)
		assertType(self, test_dict, DefaultDict)
		self.assertEqual(test_dict[0], 0)
		
	def test_deepdict(self):
		deep_dict = deepdict(self.normaldict)
		assertType(self, deep_dict, DefaultDict)
		assertType(self, deep_dict[0], dict)
		self.assertEqual(deep_dict[0], {})
		
	def test_appenddict(self):
		append_dict = appenddict(self.normaldict)
		assertType(self, append_dict, DefaultDict)
		assertType(self, append_dict[0], list)
		self.assertEqual(append_dict[0], [])
		
		
class TestCreatedUnits(TestCase):

	def setUp(self):
		units = []
		for x, y in [(0, 0), (0, 1), (0, 2)]:
			unit = gc.getPlayer(0).initUnit(0, x, y, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			units.append(unit)
			
		self.created_units = CreatedUnits(units)
		
	def tearDown(self):
		for unit in self.created_units:
			unit.kill(False, 0)
			
	def test_adjective(self):
		# given
		expected_names = ["Egyptian %s" % unit.getName() for unit in self.created_units]
		
		# when
		created_units = self.created_units.adjective('Egyptian')
		actual_names = [unit.getName() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_names, expected_names)
		
	def test_adjective_text_key(self):
		# given
		expected_names = ["Egyptian %s" % unit.getName() for unit in self.created_units]
		
		# when
		created_units = self.created_units.adjective('TXT_KEY_CIV_EGYPT_ADJECTIVE')
		actual_names = [unit.getName() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_names, expected_names)
		
	def test_adjective_empty(self):
		# given
		expected_names = [unit.getName() for unit in self.created_units]
		
		# when
		created_units = self.created_units.adjective('')
		actual_names = [unit.getName() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_names, expected_names)
	
	def test_experience(self):
		# given
		expected_experiences = [5, 5, 5]
		
		# when
		created_units = self.created_units.experience(5)
		actual_experiences = [unit.getExperience() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_experiences, expected_experiences)
		
	def test_experiences_invalid(self):
		# given
		expected_experiences = [0, 0, 0]
		
		# when
		created_units = self.created_units.experience(-5)
		actual_experiences = [unit.getExperience() for unit in self.created_units]
		
		# then
		self.assert_(isinstance(created_units, CreatedUnits))
		self.assertEqual(actual_experiences, expected_experiences)
	
	def test_one(self):
		# given
		unit = gc.getPlayer(0).initUnit(0, 1, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		created_units = CreatedUnits([unit])
		
		# when
		single_unit = created_units.one()
		
		# then
		try:
			self.assertEqual(unit.getID(), single_unit.getID())
		
		# cleanup
		finally:
			single_unit.kill(False, 0)
	
	def test_one_many_units(self):
		# when
		self.assertRaises(Exception, self.created_units.one)
	
	def test_add(self):
		unit1 = gc.getPlayer(0).initUnit(0, 1, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		unit2 = gc.getPlayer(0).initUnit(0, 1, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		units1 = CreatedUnits([unit1])
		units2 = CreatedUnits([unit2])
		
		combined = units1 + units2
		
		try:
			self.assertEqual(len(combined), 2)
			for unit in combined:
				self.assertEqual(unit in [unit1, unit2], True)
		finally:
			unit1.kill(False, -1)
			unit2.kill(False, -1)
	
	def test_one_promotion(self):
		iPromotionCombat1 = infos.type("PROMOTION_COMBAT1")
		created_units = self.created_units.promotion(iPromotionCombat1)
		
		for unit in created_units:
			self.assertEqual(unit.isHasPromotion(iPromotionCombat1), True)
	
	def test_multiple_promotions(self):
		iPromotionCombat1 = infos.type("PROMOTION_COMBAT1")
		iPromotionCombat2 = infos.type("PROMOTION_COMBAT2")
		iPromotionCombat3 = infos.type("PROMOTION_COMBAT3")
		created_units = self.created_units.promotion(iPromotionCombat1, iPromotionCombat2, iPromotionCombat3)
		
		for unit in created_units:
			self.assertEqual(unit.isHasPromotion(iPromotionCombat1), True)
			self.assertEqual(unit.isHasPromotion(iPromotionCombat2), True)
			self.assertEqual(unit.isHasPromotion(iPromotionCombat3), True)
		
		
class TestPlayers(TestCase):

	def setUp(self):
		self.players = Players([0, 1, 2])

	def test_contains_player(self):
		self.assert_(gc.getPlayer(0) in self.players)
	
	def test_contains_player_id(self):
		self.assert_(0 in self.players)
		
	def test_contains_civ_id(self):
		self.assert_(iEgypt in self.players)
		
	def test_iterate(self):
		for element in self.players:
			self.assert_(isinstance(element, int))
			self.assertEqual(gc.getPlayer(element).getID(), element)
			
	def test_string(self):
		expected_names = ','.join(['Egypt', 'Babylonia', 'Harappa'])
		actual_names = str(self.players)
		self.assertEqual(actual_names, expected_names)
		
	def test_players(self):
		expected_ids = [0, 1, 2]
		actual_ids = [player.getID() for player in self.players.players()]
		self.assertEqual(actual_ids, expected_ids)
		
	def test_alive(self):
		players = Players([0, 1, 2, 9])
		self.assert_(gc.getPlayer(9) in players)
		
		players = players.alive()
		assertType(self, players, Players)
		self.assert_(gc.getPlayer(9) not in players)
		
	def test_ai(self):
		players = self.players.ai()
		assertType(self, players, Players)
		self.assertEqual(len(players), 2)
		self.assert_(gc.getPlayer(0) not in players)

	def test_human(self):
		players = self.players.human()
		assertType(self, players, Players)
		self.assertEqual(len(players), 1)
		self.assert_(gc.getPlayer(0) in players)
		
	def test_without_player_id(self):
		players = self.players.without(0)
		assertType(self, players, Players)
		self.assertEqual(len(players), 2)
		self.assert_(gc.getPlayer(0) not in players)
		
	def test_without_list(self):
		players = self.players.without([0, 1])
		assertType(self, players, Players)
		self.assertEqual(len(players), 1)
		self.assert_(gc.getPlayer(2) in players)
		
	def test_without_set(self):
		players = self.players.without(set([0, 1]))
		assertType(self, players, Players)
		self.assertEqual(len(players), 1)
		self.assert_(gc.getPlayer(2) in players)
		
	def test_cities_none(self):
		cities = self.players.cities()
		assertType(self, cities, Cities)
		self.assertEqual(len(cities), 0)
		
	def test_cities(self):
		# given
		expected_locations = [(66, 0), (68, 0), (70, 0)]
		for i, (x, y) in enumerate(expected_locations):
			gc.getPlayer(i).initCity(x, y)
			
		# when
		cities = self.players.cities()
		assertType(self, cities, Cities)
		actual_locations = [(city.getX(), city.getY()) for city in cities]
		
		# then
		try:
			self.assertEqual(set(actual_locations), set(expected_locations))
		
		# cleanup
		finally:
			for x, y in expected_locations:
				gc.getMap().plot(x, y).getPlotCity().kill()
			
	def test_filter_by_civ(self):
		expected_players = [0]
		actual_players = self.players.civ(iEgypt)
		
		self.assertEqual(actual_players.entities(), expected_players)
		
	def test_filter_by_civs(self):
		expected_players = [0, 1]
		actual_players = self.players.civs(iEgypt, iBabylonia)
		
		self.assertEqual(set(actual_players.entities()), set(expected_players))
	
	def test_barbarian(self):
		expected_players = [0, 1, 2, 32]
		actual_players = self.players.barbarian()
		
		self.assertEqual(set(actual_players.entities()), set(expected_players))
		
	def test_independent(self):
		expected_players = [0, 1, 2, 5, 6]
		actual_players = self.players.independent()
		
		self.assertEqual(set(actual_players.entities()), set(expected_players))
	
	def test_native(self):
		expected_players = [0, 1, 2, 4]
		actual_players = self.players.native()
		
		self.assertEqual(set(actual_players.entities()), set(expected_players))
	
	def test_permutations(self):
		expected_permutations = [(0, 1), (0, 2), (1, 2)]
		actual_permutations = self.players.permutations()
		
		self.assertEqual(set(actual_permutations), set(expected_permutations))
	
	def test_permutations_identical(self):
		expected_permutations = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
		actual_permutations = self.players.permutations(identical=True)
		
		self.assertEqual(set(actual_permutations), set(expected_permutations))
		
	def test_as_civs(self):
		expected_civs = [iEgypt, iBabylonia, iHarappa]
		actual_civs = self.players.asCivs()
		
		self.assertEqual(set(actual_civs), set(expected_civs))
		
	def test_techs(self):
		gc.getTeam(gc.getPlayer(0).getTeam()).setHasTech(iWriting, True, 0, False, False)
		gc.getTeam(gc.getPlayer(0).getTeam()).setHasTech(iAlloys, True, 0, False, False)
		gc.getTeam(gc.getPlayer(1).getTeam()).setHasTech(iWriting, True, 1, False, False)
		
		has_writing = self.players.tech(iWriting)
		has_alloys = self.players.tech(iAlloys)
		
		try:
			assertType(self, has_writing, Players)
			assertType(self, has_alloys, Players)
		
			has_writing_ids = [i for i in has_writing]
			has_alloys_ids = [i for i in has_alloys]
		
			self.assertEqual(has_writing_ids, [0, 1])
			self.assertEqual(has_alloys_ids, [0])
		finally:
			gc.getTeam(gc.getPlayer(0).getTeam()).setHasTech(iWriting, False, 0, False, False)
			gc.getTeam(gc.getPlayer(0).getTeam()).setHasTech(iAlloys, False, 0, False, False)
			gc.getTeam(gc.getPlayer(1).getTeam()).setHasTech(iWriting, False, 0, False, False)
	
	def test_at_war(self):
		gc.getTeam(gc.getPlayer(0).getTeam()).declareWar(gc.getPlayer(1).getTeam(), True, -1)
		
		players0 = self.players.at_war(0)
		players1 = self.players.at_war(1)
		players2 = self.players.at_war(2)
		
		try:
			assertType(self, players0, Players)
			assertType(self, players1, Players)
			assertType(self, players2, Players)
		
			self.assertEqual(len(players0), 1)
			self.assertEqual(len(players1), 1)
			self.assertEqual(len(players2), 0)
		
			self.assert_(1 in players0)
			self.assert_(0 in players1)
		finally:
			gc.getTeam(gc.getPlayer(0).getTeam()).makePeace(gc.getPlayer(1).getTeam())
	
	def test_religion(self):
		gc.getPlayer(0).setLastStateReligion(0)
		
		players = self.players.religion(0)
		
		try:
			self.assertEqual(len(players), 1)
			self.assertEqual(players[0], 0)
		finally:
			gc.getPlayer(0).setLastStateReligion(-1)
		
	def test_can_only_contain_int_and_civ(self):
		self.assertRaises(Exception, Players, ["Egypt"])
		
	def test_can_be_built_from_civs(self):
		players = Players([iEgypt, iBabylonia])
		
		self.assert_(0 in players)
		self.assert_(1 in players)
	
	def test_defensive_pacts(self):
		gc.getTeam(gc.getPlayer(3).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), True)
		gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(3).getTeam(), True)
		
		gc.getTeam(gc.getPlayer(4).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), True)
		gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(4).getTeam(), True)
		
		gc.getTeam(gc.getPlayer(4).getTeam()).setDefensivePact(gc.getPlayer(1).getTeam(), True)
		gc.getTeam(gc.getPlayer(1).getTeam()).setDefensivePact(gc.getPlayer(4).getTeam(), True)
		
		players = self.players.defensivePacts()
		
		try:
			self.assertEqual(players.count(), 2)
			self.assert_(3 in players)
			self.assert_(4 in players)
		finally:
			gc.getTeam(gc.getPlayer(3).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), False)
			gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(3).getTeam(), False)
		
			gc.getTeam(gc.getPlayer(4).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), False)
			gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(4).getTeam(), False)
		
			gc.getTeam(gc.getPlayer(4).getTeam()).setDefensivePact(gc.getPlayer(1).getTeam(), False)
			gc.getTeam(gc.getPlayer(1).getTeam()).setDefensivePact(gc.getPlayer(4).getTeam(), False)

			
class TestPlayerFactory(TestCase):

	def setUp(self):
		self.factory = PlayerFactory()

	def test_all(self):
		players = self.factory.all()
		assertType(self, players, Players)
		self.assertEqual(len(players), 10)
		
	def test_major(self):
		players = self.factory.major()
		assertType(self, players, Players)
		self.assertEqual(len(players), 5)
		
	def test_minor(self):
		players = self.factory.minor()
		assertType(self, players, Players)
		for p in players:
			self.assert_(gc.getPlayer(p).isMinorCiv() or gc.getPlayer(p).isBarbarian())
	
	def test_vassals(self):
		# given
		gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(2, True, False)
		
		# when
		vassals = self.factory.vassals(2)
		
		# then
		try:
			assertType(self, vassals, Players)
			self.assertEqual(len(vassals), 1)
			self.assert_(gc.getPlayer(1) in vassals)
		
		# cleanup
		finally:
			gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(2, False, False)
	
	def test_none(self):
		players = self.factory.none()
		assertType(self, players, Players)
		self.assertEqual(len(players), 0)
	
	def test_of(self):
		expected_players = [0, 1, 2]
		actual_players = self.factory.of(0, 1, 2)
		
		assertType(self, actual_players, Players)
		self.assertEqual(len(actual_players), 3)
		
		for iPlayer in expected_players:
			self.assert_(iPlayer in actual_players)
	
	def test_at_war(self):
		gc.getTeam(gc.getPlayer(0).getTeam()).declareWar(gc.getPlayer(1).getTeam(), True, -1)
		
		players0 = self.factory.at_war(0)
		players1 = self.factory.at_war(1)
		players2 = self.factory.at_war(2)
		
		try:
			assertType(self, players0, Players)
			assertType(self, players1, Players)
			assertType(self, players2, Players)
		
			# note: always at war with natives and barbarians
			self.assertEqual(len(players0), 3)
			self.assertEqual(len(players1), 3)
			self.assertEqual(len(players2), 2)
		
			self.assert_(1 in players0)
			self.assert_(0 in players1)
		finally:
			gc.getTeam(gc.getPlayer(0).getTeam()).makePeace(gc.getPlayer(1).getTeam())
	
	def test_allies_with_vassal(self):
		gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(gc.getPlayer(0).getTeam(), True, False)
		
		allies = self.factory.allies(0)
		
		try:
			self.assertEqual(len(allies), 2)
			self.assert_(0 in allies)
			self.assert_(1 in allies)
		finally:
			gc.getTeam(gc.getPlayer(1).getTeam()).setVassal(gc.getPlayer(0).getTeam(), False, False)
	
	def test_allies_with_defensive_pact(self):
		gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(1).getTeam(), True)
		gc.getTeam(gc.getPlayer(1).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), True)
		
		try:
			self.assertEqual(gc.getTeam(gc.getPlayer(0).getTeam()).isDefensivePact(gc.getPlayer(1).getTeam()), True)
			self.assertEqual(gc.getTeam(gc.getPlayer(1).getTeam()).isDefensivePact(gc.getPlayer(0).getTeam()), True)
		
			allies = self.factory.allies(0)
		
			self.assertEqual(len(allies), 2)
			self.assert_(0 in allies)
			self.assert_(1 in allies)
		finally:
			gc.getTeam(gc.getPlayer(1).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), False)
			gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(1).getTeam(), False)
	
	def test_allies_with_defensive_pact_vassal(self):
		gc.getTeam(gc.getPlayer(2).getTeam()).setVassal(gc.getPlayer(1).getTeam(), True, False)
		gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(1).getTeam(), True)
		gc.getTeam(gc.getPlayer(1).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), True)
		
		allies = self.factory.allies(0)
		
		try:
			self.assertEqual(len(allies), 3)
			self.assert_(0 in allies)
			self.assert_(1 in allies)
			self.assert_(2 in allies)
		finally:
			gc.getTeam(gc.getPlayer(1).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), False)
			gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(1).getTeam(), False)
			gc.getTeam(gc.getPlayer(2).getTeam()).setVassal(gc.getPlayer(1).getTeam(), False, False)
	
	def test_defensive_pacts(self):
		gc.getTeam(gc.getPlayer(3).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), True)
		gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(3).getTeam(), True)
		
		gc.getTeam(gc.getPlayer(4).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), True)
		gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(4).getTeam(), True)
		
		players = self.factory.defensivePacts(0)
		
		try:
			self.assertEqual(len(players), 2)
			self.assert_(3 in players)
			self.assert_(4 in players)
		finally:
			gc.getTeam(gc.getPlayer(3).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), False)
			gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(3).getTeam(), False)
		
			gc.getTeam(gc.getPlayer(4).getTeam()).setDefensivePact(gc.getPlayer(0).getTeam(), False)
			gc.getTeam(gc.getPlayer(0).getTeam()).setDefensivePact(gc.getPlayer(4).getTeam(), False)


class TestUnits(TestCase):

	def setUp(self):
		units = []
		for x, y in [(0, 0), (0, 1), (0, 2), (0, 3)]:
			unit = gc.getPlayer(7).initUnit(4, x, y, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			units.append(unit)
		self.units = Units(units)
		self.unit = units[0]
			
	def tearDown(self):
		for unit in self.units:
			unit.kill(False, 3)
			
	def test_basic(self):
		assertType(self, self.units, Units)
		self.assertEqual(len(self.units), 4)
			
	def test_contains(self):
		self.assert_(self.unit in self.units)
		
	def test_contains_int(self):
		self.assertRaises(TypeError, self.units.__contains__, 0)
		
	def test_string(self):
		expected_string = "Settler (Chinese) at (0, 0), Settler (Chinese) at (0, 1), Settler (Chinese) at (0, 2), Settler (Chinese) at (0, 3)"
		self.assertEqual(str(self.units), expected_string)
		
	def test_owner(self):
		# given
		indian_unit = gc.getPlayer(8).initUnit(4, 0, 4, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		units = self.units + Units([indian_unit])
		
		# when
		indian_units = units.owner(8)
		
		# then
		try:
			assertType(self, indian_units, Units)
			self.assertEqual(len(indian_units), 1)
			self.assert_(indian_unit in indian_units)
		
		# cleanup
		finally:
			indian_unit.kill(False, -1)
		
	def test_owner_civ(self):
		# given
		indian_unit = gc.getPlayer(8).initUnit(4, 0, 4, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		units = self.units + Units([indian_unit])
		
		# when
		indian_units = units.owner(iIndia)
		
		# then
		try:
			assertType(self, indian_units, Units)
			self.assertEqual(len(indian_units), 1)
			self.assert_(indian_unit in indian_units)
		
		# cleanup
		finally:
			indian_unit.kill(False, -1)
		
	def test_type(self):
		# given
		worker = gc.getPlayer(7).initUnit(7, 0, 4, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		units = self.units + Units([worker])
		
		# when
		workers = units.type(7)
		
		# then
		try:
			assertType(self, workers, Units)
			self.assertEqual(len(workers), 1)
			self.assert_(worker in workers)

		# cleanup
		finally:
			worker.kill(False, 7)
		
	def test_by_type(self):
		# given
		worker = gc.getPlayer(7).initUnit(7, 0, 4, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		units = self.units + Units([worker])
		
		# when
		grouped = units.by_type()
		
		# then
		try:
			assertType(self, grouped, dict)
			self.assertEqual(len(grouped), 2)
			self.assert_(4 in grouped)
			self.assertEqual(len(grouped[4]), 4)
			self.assert_(7 in grouped)
			self.assertEqual(len(grouped[7]), 1)
		
		# cleanup
		finally:
			worker.kill(False, 7)
	
	def test_types(self):
		self.assertEqual(self.units.types(), [4, 4, 4, 4])
	
	def test_domain(self):
		unit = gc.getPlayer(7).initUnit(iGalley, 0, 1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		waterUnits = units.owner(7).domain(DomainTypes.DOMAIN_SEA)
		
		self.assertEqual(len(waterUnits), 1)
		
		try:
			waterUnit = waterUnits[0]
			assertType(self, waterUnit, CyUnit)
			self.assertEqual(waterUnit.getX(), 0)
			self.assertEqual(waterUnit.getY(), 1)
		finally:
			unit.kill(False, 7)
	
	def test_land(self):
		landUnits = units.owner(7).land()
		
		self.assertEqual(len(landUnits), 4)
		for unit in landUnits:
			self.assertEqual(unit.getUnitType(), 4)
	
	def test_combat(self):
		swordsman = gc.getPlayer(7).initUnit(iSwordsman, 0, 1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		archer = gc.getPlayer(7).initUnit(iArcher, 0, 1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		try:
			archers = units.owner(7).combat(UnitCombatTypes.UNITCOMBAT_ARCHER)
			self.assertEqual(len(archers), 1)
		finally:
			swordsman.kill(False, -1)
			archer.kill(False, -1)

		
class TestUnitFactory(TestCase):

	def setUp(self):
		self.factory = UnitFactory()
		self.units = []
		for _ in range(4):
			unit = gc.getPlayer(7).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			self.units.append(unit)
			
		for _ in range(3):
			unit = gc.getPlayer(8).initUnit(4, 0, 2, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			self.units.append(unit)

	def tearDown(self):
		for unit in self.units:
			unit.kill(False, unit.getOwner())

	def test_owner_id(self):
		# when
		chinese_units = self.factory.owner(7)
		
		# then
		assertType(self, chinese_units, Units)
		self.assertEqual(len(chinese_units), 4)
	
	def test_owner_civ(self):
		# when
		chinese_units = self.factory.owner(iChina)
		
		# then
		assertType(self, chinese_units, Units)
		self.assertEqual(len(chinese_units), 4)
		
	def test_owner_player(self):
		# when
		chinese_units = self.factory.owner(gc.getPlayer(7))
		
		# then
		assertType(self, chinese_units, Units)
		self.assertEqual(len(chinese_units), 4)
		
	def test_at_coordinates(self):
		# when
		indian_units = self.factory.at(0, 2)
		
		# then
		assertType(self, indian_units, Units)
		self.assertEqual(len(indian_units), 3)
		
	def test_at_plot(self):
		# when
		indian_units = self.factory.at(gc.getMap().plot(0, 2))
		
		# then
		assertType(self, indian_units, Units)
		self.assertEqual(len(indian_units), 3)
		

class TestPlots(TestCase):

	def setUp(self):
		self.tiles = [(x, y) for x in range(3) for y in range(3)]
		self.plots = Plots(self.tiles)
		
		city1 = gc.getPlayer(0).initCity(0, 3)
		city2 = gc.getPlayer(0).initCity(3, 3)
		self.cities = [city1, city2]
		
	def tearDown(self):
		for city in self.cities:
			city.kill()

	def test_basic(self):
		assertType(self, self.plots, Plots)
		self.assertEqual(len(self.plots), 9)
		
	def test_contains_tile(self):
		self.assert_((1, 1) in self.plots)
		
	def test_does_not_contain_tile(self):
		self.assert_((4, 4) not in self.plots)
		
	def test_contains_plot(self):
		self.assert_(gc.getMap().plot(1, 1) in self.plots)
		
	def test_contains_unit(self):
		unit = gc.getPlayer(3).initUnit(4, 1, 1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		try:
			self.assert_(unit in self.plots)
		finally:
			unit.kill(False, 3)
		
	def test_contains_city(self):
		city = gc.getPlayer(3).initCity(1, 1)
		
		try:
			self.assert_(city in self.plots)
		finally:
			city.kill()
		
	def test_string(self):
		self.assertEqual(str(self.plots), str(self.tiles))
		
	def test_cities(self):
		# given
		first_city = gc.getPlayer(3).initCity(0, 0)
		second_city = gc.getPlayer(3).initCity(2, 2)
		
		# when
		cities = self.plots.cities()
		
		# then
		try:
			assertType(self, cities, Cities)
			self.assertEqual(len(cities), 2)
			self.assert_(first_city in cities)
			self.assert_(second_city in cities)
		
		# cleanup
		finally:
			first_city.kill()
			second_city.kill()
		
	def test_units(self):
		# given
		tile_units = []
		for x, y in [(0, 0), (0, 2), (2, 0), (2, 2)]:
			unit = gc.getPlayer(3).initUnit(4, x, y, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			tile_units.append(unit)
		
		# when
		units = self.plots.units()
		
		# then
		try:
			assertType(self, units, Units)
			self.assertEqual(len(units), 4)
			for unit in tile_units:
				self.assert_(unit in units)
			
		# cleanup
		finally:
			for unit in tile_units:
				unit.kill(False, 3)
			
	def test_without_tile(self):
		plots = self.plots.without((1, 1))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 8)
		self.assert_((1, 1) not in plots)
		
	def test_without_tiles(self):
		plots = self.plots.without((1, 0), (1, 1), (1, 2))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 6)
		self.assert_((1, 1) not in plots)
		self.assert_((1, 2) not in plots)
		self.assert_((1, 3) not in plots)
		
	def test_without_plot(self):
		plots = self.plots.without(gc.getMap().plot(1, 1))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 8)
		self.assert_((1, 1) not in plots)
	
	def test_without_plots(self):
		plots = self.plots.without(gc.getMap().plot(1, 0), gc.getMap().plot(1, 1))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 7)
		self.assert_((1, 0) not in plots)
		self.assert_((1, 1) not in plots)
		
	def test_without_city(self):
		city = gc.getPlayer(3).initCity(1, 1)
		plots = self.plots.without(city)
		
		try:
			assertType(self, plots, Plots)
			self.assertEqual(len(plots), 8)
			self.assert_((1, 1) not in plots)
		finally:
			city.kill()
		
	def test_without_unit(self):
		unit = gc.getPlayer(3).initUnit(4, 1, 1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		plots = self.plots.without(unit)
		
		try:
			assertType(self, plots, Plots)
			self.assertEqual(len(plots), 8)
			self.assert_((1, 1) not in plots)
		finally:
			unit.kill(False, 3)
		
	def test_without_list(self):
		tiles = [(0, 0), (1, 0), (2, 0)]
		plots = self.plots.without(tiles)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 6)
		for tile in tiles:
			self.assert_(tile not in plots)
			
	def test_without_set(self):
		tiles = [(0, 0), (1, 0), (2, 0)]
		plots = self.plots.without(set(tiles))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 6)
		for tile in tiles:
			self.assert_(tile not in plots)

	def test_without_none(self):
		plots = self.plots.without(None)
		tiles = [(plot.getX(), plot.getY()) for plot in plots]
		
		assertType(self, plots, Plots)
		self.assertEqual(set(tiles), set(self.tiles))

	def test_without_empty_list(self):
		plots = self.plots.without([])
		tiles = [(plot.getX(), plot.getY()) for plot in plots]

		assertType(self, plots, Plots)
		self.assertEqual(set(tiles), set(self.tiles))

	def test_without_empty_tuple(self):
		plots = self.plots.without(())
		tiles = [(plot.getX(), plot.getY()) for plot in plots]

		assertType(self, plots, Plots)
		self.assertEqual(set(tiles), set(self.tiles))
			
	def test_closest(self):
		closest = self.plots.closest(3, 3)
		
		assertType(self, closest, CyPlot)
		self.assertEqual((closest.getX(), closest.getY()), (2, 2))
		
	def test_closest_distance(self):
		distance = self.plots.closest_distance(3, 3)
		
		assertType(self, distance, int)
		self.assertEqual(distance, 1)
	
	def test_owner(self):
		# given
		gc.getMap().plot(1, 1).setOwner(0)
		
		# when
		plots = self.plots.owner(0)
		
		# then
		try:
			assertType(self, plots, Plots)
			self.assertEqual(len(plots), 1)
			self.assert_((1, 1) in plots)
		
		# cleanup
		finally:
			gc.getMap().plot(1, 1).setOwner(-1)
		
	def test_owner_civ(self):
		# given
		gc.getMap().plot(1, 1).setOwner(0)
		
		# when
		plots = self.plots.owner(iEgypt)
		
		# then
		try:
			assertType(self, plots, Plots)
			self.assertEqual(len(plots), 1)
			self.assert_((1, 1) in plots)
		
		# cleanup
		finally:
			gc.getMap().plot(1, 1).setOwner(-1)
		
	def test_notowner(self):
		# given
		gc.getMap().plot(1, 1).setOwner(1)
		
		# when
		plots = self.plots.notowner(1)
		
		# then
		try:
			assertType(self, plots, Plots)
			self.assertEqual(len(plots), 8)
			self.assert_((1, 1) not in plots)
		
		# cleanup
		finally:
			gc.getMap().plot(1, 1).setOwner(-1)
		
	def test_notowner_civ(self):
		# given
		gc.getMap().plot(1, 1).setOwner(0)
		
		# when
		plots = self.plots.notowner(iEgypt)
		
		# then
		try:
			assertType(self, plots, Plots)
			self.assertEqual(len(plots), 8)
			self.assert_((1, 1) not in plots)
		
		# cleanup
		finally:
			gc.getMap().plot(1, 1).setOwner(-1)
	
	def test_owners(self):
		# given
		gc.getMap().plot(2, 2).setOwner(0)
		gc.getMap().plot(3, 2).setOwner(0)
		gc.getMap().plot(4, 2).setOwner(1)
		
		# when
		plots = Plots([(2, 2), (3, 2), (4, 2), (5, 2)])
		players = plots.owners()
		
		# then
		try:
			assertType(self, players, Players)
			self.assertEqual(len(players), 2)
			self.assert_(0 in players)
			self.assert_(1 in players)
			self.assert_(-1 not in players)
		
		# cleanup
		finally:
			gc.getMap().plot(2, 2).setOwner(-1)
			gc.getMap().plot(3, 2).setOwner(-1)
			gc.getMap().plot(4, 2).setOwner(-1)
		
	def test_where_surrounding(self):
		# given
		unit = gc.getPlayer(3).initUnit(4, 3, 3, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		# when
		plots = self.plots.where_surrounding(lambda p: p.getNumUnits() == 0)
		
		# then
		try:
			assertType(self, plots, Plots)
			self.assertEqual(len(plots), 8)
			self.assert_((2, 2) not in plots)
		
		# cleanup
		finally:
			unit.kill(False, 3)
		
	def test_land(self):
		plots = Plots([(64+x, 10+y) for x in range(3) for y in range(3)])
		self.assertEqual(len(plots.land()), 9)
		
	def test_no_land(self):
		self.assertEqual(len(self.plots.land()), 0)
		
	def test_water(self):
		self.assertEqual(len(self.plots.water()), 9)
		
	def test_no_water(self):
		plots = Plots([(64+x, 10+y) for x in range(3) for y in range(3)])
		self.assertEqual(len(plots.water()), 0)
		
	def test_core_player(self):
		plots = Plots([(67+x, 33+y) for x in range(3) for y in range(3)])
		self.assertEqual(len(plots.core(0)), 9)
		
	def test_no_core_player(self):
		self.assertEqual(len(self.plots.core(0)), 0)
	
	def test_core_civ(self):
		plots = Plots([(67+x, 33+y) for x in range(3) for y in range(3)])
		self.assertEqual(len(plots.core(iEgypt)), 9)
	
	def test_no_core_civ(self):
		self.assertEqual(len(self.plots.core(iEgypt)), 0)
		
	def test_any(self):
		self.assert_(self.plots.any(lambda p: p.getX() == 0))
		
	def test_not_any(self):
		self.assert_(not self.plots.any(lambda p: p.getX() == 3))
		
	def test_all(self):
		self.assert_(self.plots.all(lambda p: p.getX() < 3))
		
	def test_not_all(self):
		self.assert_(not self.plots.all(lambda p: p.getX() < 2))
		
	def test_none(self):
		self.assert_(self.plots.none(lambda p: p.getX() > 2))
		
	def test_not_none(self):
		self.assert_(not self.plots.none(lambda p: p.getX() > 1))
	
	def test_none_empty(self):
		plots = PlotFactory().of([])
		self.assertEqual(plots.none(lambda p: p.getX() > 2), True)
		
	def test_first(self):
		plot = self.plots.first()
		self.assertEqual((plot.getX(), plot.getY()), (0, 0))
		
	def test_sample(self):
		plots = self.plots.sample(3)
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 3)
		
	def test_sample_invalid_size(self):
		plots = self.plots.sample(0)
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 0)
		
	def test_sample_empty(self):
		plots = self.plots.where(lambda p: False).sample(3)
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 0)
		
	def test_buckets(self):
		x_one, y_one, rest = self.plots.buckets(lambda p: p.getX() == 1, lambda p: p.getY() == 1)
		
		assertType(self, x_one, Plots)
		assertType(self, y_one, Plots)
		assertType(self, rest, Plots)
		
		self.assertEqual(len(x_one), 3)
		self.assertEqual(len(y_one), 3)
		self.assertEqual(len(rest), 4)
		
		self.assert_(x_one.all(lambda p: p.getX() == 1))
		self.assert_(y_one.all(lambda p: p.getY() == 1))
		self.assert_(rest.all(lambda p: p.getX() != 1 and p.getY() != 1))
		
	def test_split(self):
		even, odd = self.plots.split(lambda p: (p.getX() + p.getY()) % 2 == 0)
		
		assertType(self, even, Plots)
		assertType(self, odd, Plots)
		
		self.assertEqual(len(even), 5)
		self.assertEqual(len(odd), 4)
		
		self.assert_(even.all(lambda p: (p.getX() + p.getY()) % 2 == 0))
		self.assert_(odd.all(lambda p: (p.getX() + p.getY()) % 2 == 1))
	
	def test_percentage_split(self):
		left, right = self.plots.limit(8).percentage_split(25)
		
		assertType(self, left, Plots)
		assertType(self, right, Plots)
		
		self.assertEqual(len(left), 2)
		self.assertEqual(len(right), 6)
		
		self.assertEqual(left, self.plots.limit(2))
		
	def test_sort(self):
		expected_tiles = [(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0), (1, 2), (2, 1), (2, 2)]
		
		plots = self.plots.sort(lambda p: p.getX() + p.getY())
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		assertType(self, plots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_highest(self):
		expected_tiles = [(2, 2), (1, 2), (2, 1)]
		
		plots = self.plots.highest(3, lambda p: p.getX() + p.getY())
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		assertType(self, plots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_lowest(self):
		expected_tiles = [(0, 0), (0, 1), (1, 0)]
		
		plots = self.plots.lowest(3, lambda p: p.getX() + p.getY())
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		assertType(self, plots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_including_tile(self):
		plots = self.plots.including((3, 3))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 10)
		self.assert_((3, 3) in plots)
		
	def test_including_tiles(self):
		plots = self.plots.including((3, 3), (4, 4), (5, 5))
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 12)
		for tile in [(3, 3), (4, 4), (5, 5)]:
			self.assert_(tile in plots)
			
	def test_including_plots(self):
		included = Plots([(3, 3), (4, 4), (5, 5)])
		plots = self.plots.including(included)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 12)
		for tile in [(3, 3), (4, 4), (5, 5)]:
			self.assert_(tile in plots)
	
	def test_including_inserts_at_end(self):
		plots = self.plots.including((10, 10))
		
		last_plot = plots[9]
		self.assertEqual((last_plot.getX(), last_plot.getY()), (10, 10))
			
	def test_limit(self):
		plots = self.plots.limit(3)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 3)
		for tile in [(0, 0), (0, 1), (0, 2)]:
			self.assert_(tile in plots)
			
	def test_count(self):
		self.assertEqual(self.plots.count(), 9)
		
	def test_count_condition(self):
		self.assertEqual(self.plots.count(lambda p: p.getX() == 0), 3)
		
	def test_maximum(self):
		max = self.plots.maximum(lambda p: p.getX() + p.getY())
		
		assertType(self, max, CyPlot)
		self.assertEqual((max.getX(), max.getY()), (2, 2))
		
	def test_rank(self):
		rank = self.plots.rank((2, 2), lambda p: p.getX() * p.getY())
		
		assertType(self, rank, int)
		self.assertEqual(rank, 0)
		
	def test_shuffle(self):
		plots = self.plots.shuffle()
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 9)
		self.assert_(plots != self.plots)
		
	def test_fraction(self):
		plots = self.plots.fraction(3)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 3)
		self.assertEqual(plots, self.plots.limit(3))
		
	def test_percentage(self):
		plots = self.plots.limit(5).percentage(60)
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 3)
		self.assertEqual(plots, self.plots.limit(3))
		
	def test_sum(self):
		sum = self.plots.sum(lambda p: p.getX() + p.getY())
		
		assertType(self, sum, int)
		self.assertEqual(sum, 18)
	
	def test_average(self):
		average = self.plots.average(lambda p: p.getX() + p.getY())
		
		assertType(self, average, float)
		self.assertEqual(average, 2.0)
	
	def test_average_empty(self):
		plots = Plots([])
		average = plots.average(lambda p: p.getX() + p.getY())
		
		assertType(self, average, float)
		self.assertEqual(average, 0.0)
		
	def test_accessor(self):
		plot = self.plots[0]
		
		assertType(self, plot, CyPlot)
		self.assertEqual((plot.getX(), plot.getY()), (0, 0))
		
	def test_add(self):
		added = Plots([(0, 3), (1, 3), (2, 3)])
		plots = self.plots + added
		
		assertType(self, plots, Plots)
		self.assertEqual(len(plots), 12)
		for tile in [(x, y) for x in range(3) for y in range(4)]:
			self.assert_(tile in plots)
			
	def test_add_other_class(self):
		added = Cities(self.cities)
		self.assertRaises(TypeError, self.plots.__add__, added)
		
	def test_string(self):
		expected_string = str(self.tiles)
		actual_string = str(self.plots)
		self.assertEqual(actual_string, expected_string)
		
	def test_same(self):
		self.assert_(self.plots.same(self.plots.shuffle()))
		
	def test_equal(self):
		plots = Plots(self.tiles)
		self.assertEqual(self.plots, plots)
		
	def test_unequal_with_different_order(self):
		plots = self.plots.sort(lambda p: p.getY())
		self.assert_(self.plots != plots)
		
	def test_equal_other_class(self):
		cities = Cities(self.cities)
		self.assert_(self.plots != cities)
	
	def test_unequal_none(self):
		self.assert_(self.plots != None)
		
	def test_greater_than_plots(self):
		plots = self.plots.including((3, 3))
		self.assert_(plots > self.plots)
		
	def test_greater_than_int(self):
		self.assert_(self.plots > 8)
		
	def test_greater_than_other_class(self):
		cities = Cities(self.cities)
		self.assertRaises(TypeError, self.plots.__gt__, cities)
		
	def test_greater_equal_plots(self):
		plots = self.plots.including((3, 3))
		self.assert_(plots >= self.plots)
		
	def test_greater_equal_int(self):
		self.assert_(self.plots >= 9)
		self.assert_(self.plots >= 8)
		
	def test_greater_equal_other_class(self):
		cities = Cities(self.cities)
		self.assertRaises(TypeError, self.plots.__ge__, cities)
		
	def test_less_than_plots(self):
		plots = self.plots.including((3, 3))
		self.assert_(self.plots < plots)
		
	def test_less_than_int(self):
		self.assert_(self.plots < 10)
		
	def test_less_than_other_class(self):
		cities = Cities(self.cities)
		self.assertRaises(TypeError, self.plots.__lt__, cities)
		
	def test_less_equal_plots(self):
		plots = self.plots.including((3, 3))
		self.assert_(self.plots <= plots)
		
	def test_less_equal_int(self):
		self.assert_(self.plots <= 9)
		self.assert_(self.plots <= 10)
		
	def test_less_equal_other_class(self):
		cities = Cities(self.cities)
		self.assertRaises(TypeError, self.plots.__le__, cities)
		
	def test_iterate_all_does_not_contain_invalid(self):
		for plot in plots.all():
			self.assert_((plot.getX(), plot.getY()) != (-1, -1))
			
	def test_regions(self):
		tiles = [(23, 37), (26, 38), (26, 40)] # mesoamerica, caribbean, usa
		plots = Plots(tiles)
		
		expected_tiles = [(23, 37), (26, 38)]
		actual_plots = plots.regions(rCaribbean, rMesoamerica)
		actual_tiles = [(plot.getX(), plot.getY()) for plot in actual_plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
	
	def test_unique(self):
		tiles = [(0, 0), (0, 0), (1, 1), (1, 1), (1, 1), (2, 2)]
		plots = Plots(tiles)
		
		self.assertEqual(len(plots.unique()), 3)
		self.assert_((0, 0) in plots)
		self.assert_((1, 1) in plots)
		self.assert_((2, 2) in plots)
	
	def test_no_enemies(self):
		unit0 = gc.getPlayer(0).initUnit(iArcher, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		unit1 = gc.getPlayer(1).initUnit(iArcher, 0, 1, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		unit2 = gc.getPlayer(2).initUnit(iArcher, 0, 2, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		gc.getTeam(0).setAtWar(1, True)
		
		plots = self.plots.no_enemies(0)
		
		self.assertEqual(len(plots), 8)
		self.assert_((0, 0) in plots)
		self.assert_((0, 1) not in plots)
		self.assert_((0, 2) in plots)
		
		unit0.kill(False, -1)
		unit1.kill(False, -1)
		unit2.kill(False, -1)
		
		gc.getTeam(0).setAtWar(1, False)

	def test_enrich(self):
		tiles = [(0, 0), (0, 1), (0, 2)]
		testPlots = Plots(tiles)
		
		enriched = testPlots.enrich(lambda (x, y): plots.of([(x+1, y)]))
		
		self.assertEqual(len(enriched), 6)
		self.assert_((1, 0) in enriched)
		self.assert_((1, 1) in enriched)
		self.assert_((1, 2) in enriched)
	
	def test_enrich_unique(self):
		tiles = [(0, 0)]
		testPlots = Plots(tiles)
		
		func = lambda (x, y): plots.of([(x+1, y)])
		enriched = testPlots.enrich(func).enrich(func)
		
		self.assertEqual(len(enriched), 3)
		self.assert_((0, 0) in enriched)
		self.assert_((1, 0) in enriched)
		self.assert_((2, 0) in enriched)
	
	def test_no_name(self):
		self.assertEqual(self.plots.name(), "")
	
	def test_named(self):
		plots = self.plots.named("EUROPE")
		
		assertType(self, plots, Plots)
		self.assertEqual(plots.name(), "Europe")
	
	def test_name_preserved_by_transformation(self):
		plots = self.plots.named("EUROPE")
		self.assertEqual(plots.name(), "Europe")
		
		plots = self.plots.where(lambda p: p.getX() == 1)
		self.assertEqual(plots.name(), "Europe")
	
	def test_all_if_any_empty(self):
		plots = Plots([])
		self.assertEqual(plots.all_if_any(lambda plot: plot.getX() >= 0), False)
	
	def test_all_if_any_all(self):
		self.assertEqual(self.plots.all_if_any(lambda plot: plot.getX() >= 0), True)
	
	def test_all_if_any_some(self):
		self.assertEqual(self.plots.all_if_any(lambda plot: plot.getX() >= 2), False)
	
	def test_take_less(self):
		first, second, third = self.plots.take(3)
		
		assertType(self, first, CyPlot)
		self.assertEqual((first.getX(), first.getY()), (0, 0))
		
		assertType(self, second, CyPlot)
		self.assertEqual((second.getX(), second.getY()), (0, 1))
		
		assertType(self, third, CyPlot)
		self.assertEqual((third.getX(), third.getY()), (0, 2))
	
	def test_take_more(self):
		taken = self.plots.take(10)
		
		self.assertEqual(taken[-1], None)
		assertType(self, taken[-2], CyPlot)
	
	def test_expand(self):
		area = PlotFactory().of([(1, 1), (2, 1)])
		
		expectedExpanded = PlotFactory().of([(x, y) for x in range(4) for y in range(3)])
		actualExpanded = area.expand(1)
		
		self.assertEqual(actualExpanded.same(expectedExpanded), True)
	
	def test_edge(self):
		tiles = [(50+x, 50+y) for x in range(3) for y in range(3)]
		area = PlotFactory().of(tiles)
		
		expectedTiles = [(50, 50), (50, 51), (50, 52), (51, 50), (51, 52), (52, 50), (52, 51), (52, 52)]
		
		edge = area.edge()
		
		self.assertEqual(edge.count(), len(expectedTiles))
		for tile in expectedTiles:
			self.assertEqual(tile in edge, True)
	
	def test_grouped(self):
		grouped = list(self.plots.grouped(lambda plot: (plot.getX() + plot.getY()) % 2))
		
		expectedEven = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
		expectedOdd = [(0, 1), (1, 0), (1, 2), (2, 1)]
		
		self.assertEqual(len(grouped), 2)
		evenGroup, oddGroup = grouped
		
		evenKey, evenValues = evenGroup
		self.assertEqual(evenKey, 0)
		assertType(self, evenValues, Plots)
		self.assertEqual([(p.getX(), p.getY()) for p in evenValues], expectedEven)
		
		oddKey, oddValues = oddGroup
		self.assertEqual(oddKey, 1)
		assertType(self, oddValues, Plots)
		self.assertEqual([(p.getX(), p.getY()) for p in oddValues], expectedOdd)
	
	def test_closest_all(self):
		other_plots = PlotFactory().of([(4, 4), (4, 5), (5, 4), (5, 5)])
		
		closest_plot = self.plots.closest_all(other_plots)
		closest_other_plot = other_plots.closest_all(self.plots)
		
		self.assertEqual((closest_plot.getX(), closest_plot.getY()), (2, 2))
		self.assertEqual((closest_other_plot.getX(), closest_other_plot.getY()), (4, 4))
	
	def test_closest_all_overlap(self):
		other_plots = PlotFactory().of([(2, 2), (2, 3), (3, 2), (3, 3)])
		
		closest_plot = self.plots.closest_all(other_plots)
		closest_other_plot = other_plots.closest_all(self.plots)
		
		self.assertEqual((closest_plot.getX(), closest_plot.getY()), (2, 2))
		self.assertEqual((closest_other_plot.getX(), closest_other_plot.getY()), (2, 2))
	
	def test_closest_all_empty(self):
		other_plots = PlotFactory().none()
		
		closest_plot = self.plots.closest_all(other_plots)
		closest_other_plot = other_plots.closest_all(self.plots)
		
		self.assertEqual(closest_plot, None)
		self.assertEqual(closest_other_plot, None)
	
	def test_closest_all_not_locations(self):
		other_plots = [(2, 2), (2, 3)]
		
		self.assertRaises(Exception, self.plots.closest_all, other_plots)
		
	def test_closest_within_match(self):
		closest_within = self.plots.closest_within((2, 2))
		
		assertType(self, closest_within, Plots)
		self.assertEqual(closest_within.count(), 1)
		self.assertEqual((closest_within[0].getX(), closest_within[0].getY()), (2, 2))
	
	def test_closest_within_outside(self):
		closest_within = self.plots.closest_within((3, 1))
		
		expected_tiles = [(2, 0), (2, 1), (2, 2)]
		
		assertType(self, closest_within, Plots)
		self.assertEqual(closest_within.count(), 3)
		
		actual_tiles = [(p.getX(), p.getY()) for p in closest_within]
		
		self.assertEqual(actual_tiles, expected_tiles)
	
	def test_closest_within_outside_radius(self):
		closest_within = self.plots.closest_within((4, 1), radius=2)
		
		expected_tiles = [(2, 0), (2, 1), (2, 2)]
		
		assertType(self, closest_within, Plots)
		self.assertEqual(closest_within.count(), 3)
		
		actual_tiles = [(p.getX(), p.getY()) for p in closest_within]
		
		self.assertEqual(actual_tiles, expected_tiles)
	
	def test_closest_within_outside_radius_closer(self):
		closest_within = self.plots.closest_within((3, 1), radius=2)
		
		expected_tiles = [(2, 0), (2, 1), (2, 2)]
		
		assertType(self, closest_within, Plots)
		self.assertEqual(closest_within.count(), 3)
		
		actual_tiles = [(p.getX(), p.getY()) for p in closest_within]
		
		self.assertEqual(actual_tiles, expected_tiles)
	
	def test_closest_within_empty(self):
		closest_within = self.plots.closest_within((4, 1), radius=1)
		
		assertType(self, closest_within, Plots)
		self.assertEqual(closest_within.count(), 0)
		
	def test_area(self):
		africaTile = (48, 30)
		americaTile = (37, 28)
		
		plots = PlotFactory().of([africaTile, americaTile])
		
		africaID = plot(africaTile).getArea()
		africaPlots = plots.area(africaID)
		
		assertType(self, africaPlots, Plots)
		self.assertEqual(africaPlots.count(), 1)
		self.assertEqual((africaPlots[0].getX(), africaPlots[0].getY()), africaTile)
	
	def test_area_tile(self):
		africaTile = (48, 30)
		americaTile = (37, 28)
		
		plots = PlotFactory().of([africaTile, americaTile])
		
		africaPlots = plots.area(africaTile)
		
		assertType(self, africaPlots, Plots)
		self.assertEqual(africaPlots.count(), 1)
		self.assertEqual((africaPlots[0].getX(), africaPlots[0].getY()), africaTile)
	
	def test_area_plot(self):
		africaTile = (48, 30)
		americaTile = (37, 28)
		
		plots = PlotFactory().of([africaTile, americaTile])
		
		africaPlot = plot(africaTile)
		africaPlots = plots.area(africaPlot)
		
		assertType(self, africaPlots, Plots)
		self.assertEqual(africaPlots.count(), 1)
		self.assertEqual((africaPlots[0].getX(), africaPlots[0].getY()), africaTile)
	
	def test_area_city(self):
		africaTile = (48, 30)
		americaTile = (37, 28)
		
		plots = PlotFactory().of([africaTile, americaTile])
		
		africaCity = gc.getPlayer(0).initCity(*africaTile)
		africaPlots = plots.area(africaCity)
		
		try:
			assertType(self, africaPlots, Plots)
			self.assertEqual(africaPlots.count(), 1)
			self.assertEqual((africaPlots[0].getX(), africaPlots[0].getY()), africaTile)
		finally:
			africaCity.kill()
		
	def test_areas(self):
		africaTile = (48, 30)
		americaTile = (37, 28)
		australiaTile = (117, 11)
		
		plots = PlotFactory().of([africaTile, americaTile, australiaTile])
		
		africaID = plot(africaTile).getArea()
		americaID = plot(americaTile).getArea()
		areaPlots = plots.areas(africaID, americaID)
		
		actual_tiles = [(p.getX(), p.getY()) for p in areaPlots]
		expected_tiles = [africaTile, americaTile]
		
		assertType(self, areaPlots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
	
	def test_areas_tiles(self):
		africaTile = (48, 30)
		americaTile = (37, 28)
		australiaTile = (117, 11)
		
		plots = PlotFactory().of([africaTile, americaTile, australiaTile])
		
		areaPlots = plots.areas(africaTile, americaTile)
		
		actual_tiles = [(p.getX(), p.getY()) for p in areaPlots]
		expected_tiles = [africaTile, americaTile]
		
		assertType(self, areaPlots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
	
	def test_areas_plots(self):
		africaTile = (48, 30)
		americaTile = (37, 28)
		australiaTile = (117, 11)
		
		plots = PlotFactory().of([africaTile, americaTile, australiaTile])
		
		africaPlot = plot(africaTile)
		americaPlot = plot(americaTile)
		areaPlots = plots.areas(africaPlot, americaPlot)
		
		actual_tiles = [(p.getX(), p.getY()) for p in areaPlots]
		expected_tiles = [africaTile, americaTile]
		
		assertType(self, areaPlots, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
	
	def test_areas_cities(self):
		africaTile = (48, 30)
		americaTile = (37, 28)
		australiaTile = (117, 11)
		
		plots = PlotFactory().of([africaTile, americaTile, australiaTile])
		
		africaCity = gc.getPlayer(0).initCity(*africaTile)
		americaCity = gc.getPlayer(0).initCity(*americaTile)
		areaPlots = plots.areas(africaCity, americaCity)
		
		actual_tiles = [(p.getX(), p.getY()) for p in areaPlots]
		expected_tiles = [africaTile, americaTile]
		
		try:
			assertType(self, areaPlots, Plots)
			self.assertEqual(actual_tiles, expected_tiles)
		finally:
			africaCity.kill()
			americaCity.kill()
	
	def test_intersect(self):
		left = PlotFactory().of([(0, 0), (0, 1)])
		right = PlotFactory().of([(0, 1), (0, 2)])
		
		self.assertEqual(left.intersect(right), True)
		self.assertEqual(right.intersect(left), True)
	
	def test_not_intersect(self):
		left = PlotFactory().of([(0, 0)])
		right = PlotFactory().of([(0, 1)])
		
		self.assertEqual(left.intersect(right), False)
		self.assertEqual(right.intersect(left), False)
	
	def test_intersect_equal(self):
		left = PlotFactory().of([(0, 0)])
		right = PlotFactory().of([(0, 0)])
		
		self.assertEqual(left.intersect(right), True)
		self.assertEqual(right.intersect(left), True)


class TestPlotFactory(TestCase):

	def setUp(self):
		self.factory = PlotFactory()
		
	def test_of(self):
		tiles = [(0, 0), (0, 1), (0, 2)]
		self.assertEqual(self.factory.of(tiles), Plots(tiles))
		
	def test_rectangle(self):
		plots = self.factory.rectangle((0, 0), (2, 2))
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		self.assertEqual(plots, Plots(expected_tiles))
		
	def test_rectangle_inverted(self):
		plots = self.factory.rectangle((2, 2), (0, 0))
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		self.assertEqual(plots, Plots(expected_tiles))
		
	def test_rectangle_diagonal(self):
		plots = self.factory.rectangle((0, 2), (2, 0))
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		self.assertEqual(plots, Plots(expected_tiles))
		
	def test_rectangle_plots(self):
		plots = self.factory.rectangle(gc.getMap().plot(0, 0), gc.getMap().plot(2, 2))
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		self.assertEqual(plots, Plots(expected_tiles))
		
	def test_all(self):
		plots = self.factory.all()
		self.assertEqual(len(plots), iWorldX * iWorldY)
		
	def test_region(self):
		expected_tiles = [(25, 38), (26, 38), (27, 38), (27, 36), (29, 37), (30, 37), (30, 39), (32, 37), (33, 33), (33, 35)]
		region = Plots(expected_tiles)
		plots = self.factory.region(rCaribbean)
		self.assertEqual(len(region), len(plots))
		self.assert_(plots.same(region))
		
	def test_regions_single(self):
		self.assert_(self.factory.region(rCaribbean).same(self.factory.regions(rCaribbean)))
	
	def test_regions_multiple(self):
		self.assert_(self.factory.regions(rEgypt, rMesopotamia).same(self.factory.region(rEgypt) + self.factory.region(rMesopotamia)))
	
	def test_surrounding(self):
		expected_tiles = [(x, y) for x in range(3) for y in range(3)]
		plots = self.factory.surrounding((1, 1))
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_surrounding_wrap(self):
		expected_tiles = [(0, 0), (1, 0), (0, 1), (1, 1), (123, 0), (123, 1)]
		plots = self.factory.surrounding((0, 0))
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_surrounding_radius(self):
		expected_tiles = [(x, y) for x in range(5) for y in range(5)]
		plots = self.factory.surrounding((2, 2), radius=2)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_surrounding_zero(self):
		expected_tiles = [(1, 1)]
		plots = self.factory.surrounding((1, 1), radius=0)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_surrounding_negative(self):
		self.assertRaises(ValueError, self.factory.surrounding, 1, 1, radius=-1)
		
	def test_ring(self):
		expected_tiles = [(x, y) for x in range(3) for y in range(3) if (x, y) != (1, 1)]
		plots = self.factory.ring(1, 1, radius=1)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		self.assertEqual((1, 1) in plots, False)
		
	def test_ring_large(self):
		expected_tiles = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (1, 4), (2, 4), (3, 4)]
		plots = self.factory.ring(2, 2, radius=2)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
	
	def test_circle(self):
		expected_tiles = [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3)]
		plots = self.factory.circle(2, 2, radius=2)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_owner(self):
		gc.getMap().plot(0, 0).setOwner(0)
		gc.getMap().plot(1, 0).setOwner(0)
		
		expected_tiles = [(0, 0), (1, 0)]
		plots = self.factory.owner(0)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		try:
			self.assertEqual(set(actual_tiles), set(expected_tiles))
		finally:
			gc.getMap().plot(0, 0).setOwner(-1)
			gc.getMap().plot(1, 0).setOwner(-1)
		
	def test_owner_civ(self):
		gc.getMap().plot(0, 0).setOwner(0)
		gc.getMap().plot(1, 0).setOwner(0)
		
		expected_tiles = [(0, 0), (1, 0)]
		plots = self.factory.owner(iEgypt)
		
		actual_tiles = [(p.getX(), p.getY()) for p in plots]
		
		try:
			self.assertEqual(set(actual_tiles), set(expected_tiles))
		finally:
			gc.getMap().plot(0, 0).setOwner(-1)
			gc.getMap().plot(1, 0).setOwner(-1)
	
	def test_birth(self):
		plots = self.factory.birth(iEgypt)
		assertType(self, plots, Plots)
		
	def test_respawn(self):
		plots = self.factory.birth(iEgypt)
		assertType(self, plots, Plots)
		
	def test_core(self):
		plots = self.factory.core(iEgypt)
		assertType(self, plots, Plots)
		
	def test_normal(self):
		plots = self.factory.normal(iEgypt)
		assertType(self, plots, Plots)
		
	def test_broader(self):
		plots = self.factory.broader(iEgypt)
		assertType(self, plots, Plots)
		
	def test_capital(self):
		plot = self.factory.capital(iEgypt)
		assertType(self, plot, CyPlot)
		
	def test_newCapital(self):
		plot = self.factory.newCapital(iEgypt)
		assertType(self, plot, CyPlot)
		
	def test_respawnCapital(self):
		plot = self.factory.respawnCapital(iEgypt)
		assertType(self, plot, CyPlot)
		
	def test_city_radius(self):
		city = gc.getPlayer(0).initCity(70, 30)
		
		expected_plots = sorted([
					  (69, 32), (70, 32), (71, 32),
			(68, 31), (69, 31), (70, 31), (71, 31), (72, 31),
			(68, 30), (69, 30), (70, 30), (71, 30), (72, 30),
			(68, 29), (69, 29), (70, 29), (71, 29), (72, 29),
			          (69, 28), (70, 28), (71, 28)
		])
		
		actual_plots = self.factory.city_radius(city)
		sorted_actual_plots = sorted([(plot.getX(), plot.getY()) for plot in actual_plots])
		
		try:
			self.assertEqual(sorted_actual_plots, expected_plots)
		finally:
			city.kill()
	
	def test_sum(self):
		area1 = self.factory.of([(0, 0), (0, 1)])
		area2 = self.factory.of([(0, 2), (0, 3)])
		
		combined = self.factory.sum([area1, area2])
		
		actual_tiles = [(p.getX(), p.getY()) for p in combined]
		expected_tiles = [(0, 0), (0, 1), (0, 2), (0, 3)]
		
		assertType(self, combined, Plots)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_sum_empty(self):
		combined = self.factory.sum([])
		
		assertType(self, combined, Plots)
		self.assertEqual(combined.count(), 0)
	
	def test_sum_one(self):
		tiles = [(0, 0), (0, 1)]
		area = self.factory.of(tiles)
		
		combined = self.factory.sum([area])
		
		actual_tiles = [(p.getX(), p.getY()) for p in combined]
		
		assertType(self, combined, Plots)
		self.assertEqual(actual_tiles, tiles)

class TestCities(TestCase):

	def setUp(self):
		city1 = gc.getPlayer(7).initCity(0, 0)
		city2 = gc.getPlayer(7).initCity(0, 2)
		city3 = gc.getPlayer(8).initCity(2, 0)
		
		self.cities = Cities([city1, city2, city3])
		
	def tearDown(self):
		for city in self.cities:
			city.kill()
			
	def test_basic(self):
		assertType(self, self.cities, Cities)
		self.assertEqual(len(self.cities), 3)
		
	def test_contains_tile(self):
		self.assert_((0, 0) in self.cities)
		
	def test_contains_plot(self):
		self.assert_(gc.getMap().plot(0, 0) in self.cities)
		
	def test_contains_city(self):
		self.assert_(gc.getMap().plot(0, 0).getPlotCity() in self.cities)
		
	def test_contains_unit(self):
		unit = gc.getPlayer(3).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		try:
			self.assert_(unit in self.cities)
		finally:
			unit.kill(False, 3)
		
	def test_contains_other(self):
		self.assertRaises(TypeError, self.cities.__contains__, 0)
		
	def test_without_tile(self):
		cities = self.cities.without((0, 0))
		expected_tiles = [(0, 2), (2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_plot(self):
		cities = self.cities.without(gc.getMap().plot(0, 0))
		expected_tiles = [(0, 2), (2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_city(self):
		cities = self.cities.without(gc.getMap().plot(0, 0).getPlotCity())
		expected_tiles = [(0, 2), (2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_list(self):
		cities = self.cities.without([(0, 2), (2, 0)])
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_cities(self):
		city1 = self.cities[1]
		city2 = self.cities[2]
	
		subtracted = Cities([city1, city2])
		cities = self.cities.without(subtracted)
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_without_plots(self):
		subtracted = plots.rectangle((0, 0), (1, 2))
		cities = self.cities.without(subtracted)
		expected_tiles = [(2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_religion(self):
		self.cities[0].setHasReligion(0, True, False, False)
		cities = self.cities.religion(0)
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_owner(self):
		cities = self.cities.owner(7)
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_owner_civ(self):
		cities = self.cities.owner(iChina)
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
	
	def test_owners(self):
		# given
		city1 = gc.getPlayer(0).initCity(2, 2)
		city2 = gc.getPlayer(0).initCity(4, 2)
		city3 = gc.getPlayer(1).initCity(6, 2)
		
		# when
		cities = CityFactory().of([(2, 2), (4, 2), (6, 2), (8, 2)])
		players = cities.owners()
		
		# then
		try:
			assertType(self, players, Players)
			self.assertEqual(len(players), 2)
			self.assert_(0 in players)
			self.assert_(1 in players)
		
		# cleanup
		finally:
			city1.kill()
			city2.kill()
			city3.kill()
		
	def test_building(self):
		self.cities[0].setHasRealBuilding(iFactory, True)
		cities = self.cities.building(iFactory)
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_building_effect(self):
		self.cities[0].setHasRealBuilding(iFactory, True)
		cities = self.cities.building_effect(iFactory)
		expected_tiles = [(0, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_core_player(self):
		city = gc.getPlayer(0).initCity(69, 33)
		cities = self.cities.including(city)
		self.assertEqual(len(cities), 4)
		
		actual_cities = cities.core(0)
		expected_tiles = [(69, 33)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in actual_cities]
		
		try:
			assertType(self, cities, Cities)
			self.assertEqual(actual_tiles, expected_tiles)
		finally:
			city.kill()
	
	def test_core_civ(self):
		city = gc.getPlayer(0).initCity(69, 33)
		cities = self.cities.including(city)
		self.assertEqual(len(cities), 4)
		
		actual_cities = cities.core(iEgypt)
		expected_tiles = [(69, 33)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in actual_cities]
		
		try:
			assertType(self, cities, Cities)
			self.assertEqual(actual_tiles, expected_tiles)
		finally:
			city.kill()
			
	def test_coastal(self):
		city = gc.getPlayer(0).initCity(63, 10)
		cities = self.cities.including(city)
		actual_cities = cities.coastal()
		expected_tiles = [(63, 10)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in actual_cities]
		
		try:
			assertType(self, cities, Cities)
			self.assertEqual(actual_tiles, expected_tiles)
		finally:
			city.kill()
		
	def test_regions(self):
		tiles = [(23, 37), (26, 38), (26, 40)] # mesoamerica, caribbean, usa
		created_cities = []
		for x, y in tiles:
			city = gc.getPlayer(0).initCity(x, y)
			created_cities.append(city)
		
		cities = Cities(created_cities)
		
		expected_tiles = [(23, 37), (26, 38)]
		actual_cities = cities.regions(rCaribbean, rMesoamerica)
		actual_tiles = [(city.getX(), city.getY()) for city in actual_cities]
		
		try:
			self.assertEqual(set(actual_tiles), set(expected_tiles))
		finally:
			for city in created_cities:
				city.kill()
			
	def test_notowner(self):
		expected_tiles = [(2, 0)]
		
		cities = self.cities.notowner(7)
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_notowner_civ(self):
		expected_tiles = [(2, 0)]
		
		cities = self.cities.notowner(iChina)
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_existing(self):
		city = gc.getPlayer(0).initCity(4, 4)
		
		cities = CityFactory().of([(4, 4)])
		
		self.assertEqual(len(cities), 1)
		self.assertEqual(len(cities.existing()), 1)
		
		city.kill()
		
		self.assertEqual(len(cities), 1)
		self.assertEqual(len(cities.existing()), 0)
		
		
class TestCityFactory(TestCase):

	def setUp(self):
		gc.getPlayer(7).initCity(0, 0)
		gc.getPlayer(7).initCity(0, 2)
		gc.getPlayer(8).initCity(2, 0)
		
		self.factory = CityFactory()
		
	def tearDown(self):
		for x, y in [(0, 0), (0, 2), (2, 0)]:
			gc.getMap().plot(x, y).getPlotCity().kill()
			
	def test_owner(self):
		cities = self.factory.owner(7)
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_owner_civ(self):
		cities = self.factory.owner(iChina)
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_all(self):
		cities = self.factory.all()
		expected_tiles = [(0, 0), (0, 2), (2, 0)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(set(actual_tiles), set(expected_tiles))
		
	def test_rectangle(self):
		cities = self.factory.rectangle((0, 0), (1, 2))
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_region(self):
		caribbean = plots.region(rCaribbean).random()
		city = gc.getPlayer(7).initCity(caribbean.getX(), caribbean.getY())
		
		cities = self.factory.region(rCaribbean)
		
		try:
			assertType(self, cities, Cities)
			self.assertEqual(len(cities), 1)
			self.assert_(city in cities)
		finally:
			city.kill()
		
	def test_of(self):
		cities = self.factory.of([(0, 0), (0, 1), (0, 2)])
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
	def test_surrounding(self):
		cities = self.factory.surrounding((0, 1))
		expected_tiles = [(0, 0), (0, 2)]
		
		actual_tiles = [(city.getX(), city.getY()) for city in cities]
		
		assertType(self, cities, Cities)
		self.assertEqual(actual_tiles, expected_tiles)
		
		
class TestMove(TestCase):

	def setUp(self):
		self.unit = gc.getPlayer(3).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
	def tearDown(self):
		if self.unit.getX() >= 0:
			self.unit.kill(False, 3)

	def test_move_tile(self):
		move(self.unit, (0, 2))
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 2))
		
	def test_move_plot(self):
		move(self.unit, gc.getMap().plot(0, 2))
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 2))
		
	def test_move_city(self):
		city = gc.getPlayer(3).initCity(0, 2)
		move(self.unit, city)
		
		try:
			self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 2))
		finally:
			city.kill()
		
	def test_move_no_destination(self):
		move(self.unit, None)
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 0))
		
	def test_move_invalid_location(self):
		self.unit.kill(False, 3)
		move(self.unit, (0, 2))
		self.assertEqual((self.unit.getX(), self.unit.getY()), (-2147483647, -2147483647))
		
	def test_move_same_destination(self):
		move(self.unit, (0, 0))
		self.assertEqual((self.unit.getX(), self.unit.getY()), (0, 0))
	

class TestHasCivic(TestCase):

	def test_has_civic(self):
		self.assert_(has_civic(1, 0))
		
	def test_not_has_civic(self):
		self.assert_(not has_civic(1, 1))
		
	def test_has_civic_player(self):
		self.assert_(has_civic(gc.getPlayer(1), 0))
		
		
class TestScenarioUtils(TestCase):

	def test_scenario(self):
		self.assertEqual(scenario(), i3000BC)
		
	def test_scenario_start_turn(self):
		self.assertEqual(scenarioStartTurn(), 0)
		
	def test_scenario_start_year(self):
		self.assertEqual(scenarioStartYear(), -3000)
		
		
class TestUniqueUnitsAndBuildings(TestCase):

	def test_base_building_for_base(self):
		self.assertEqual(base_building(iMonument), iMonument)
		
	def test_base_building_for_unique(self):
		self.assertEqual(base_building(iObelisk), iMonument)
		
	def test_base_building_for_none(self):
		self.assertEqual(base_building(None), None)
		
	def test_unique_building_for_base(self):
		self.assertEqual(unique_building(0, iMonument), iObelisk)
		
	def test_unique_building_for_unique(self):
		self.assertEqual(unique_building(0, iObelisk), iObelisk)
		
	def test_unique_building_no_player(self):
		self.assertEqual(unique_building(-1, iObelisk), iMonument)
		
	def test_unique_building_for_base_civ(self):
		self.assertEqual(unique_building(iEgypt, iMonument), iObelisk)
	
	def test_unique_building_for_unique_civ(self):
		self.assertEqual(unique_building(iEgypt, iObelisk), iObelisk)
		
	def test_unique_building_no_civ(self):
		self.assertEqual(unique_building(NoCiv, iObelisk), iMonument)
		
	def test_base_unit_for_base(self):
		self.assertEqual(base_unit(iChariot), iChariot)
		
	def test_base_unit_for_unique(self):
		self.assertEqual(base_unit(iWarChariot), iChariot)
		
	def test_unique_unit_for_base(self):
		self.assertEqual(unique_unit(0, iChariot), iWarChariot)
		
	def test_unique_unit_for_unique(self):
		self.assertEqual(unique_unit(0, iWarChariot), iWarChariot)
		
	def test_unique_unit_no_player(self):
		self.assertEqual(unique_unit(-1, iWarChariot), iChariot)
	
	def test_unique_unit_for_base_civ(self):
		self.assertEqual(unique_unit(iEgypt, iChariot), iWarChariot)
	
	def test_unique_unit_for_unique_civ(self):
		self.assertEqual(unique_unit(iEgypt, iWarChariot), iWarChariot)
	
	def test_unique_unit_no_civ(self):
		self.assertEqual(unique_unit(NoCiv, iWarChariot), iChariot)
		

class TestMasterAndVassal(TestCase):
	
	def test_master(self):
		gc.getTeam(gc.getPlayer(0).getTeam()).setVassal(1, True, False)
		
		self.assert_(gc.getTeam(0).isVassal(1))
		
		try:
			self.assertEqual(master(0), 1)
		finally:
			gc.getTeam(gc.getPlayer(0).getTeam()).setVassal(1, False, False)
		
	def test_master_no_vassal(self):
		self.assertEqual(master(1), None)
		
	def test_vassals(self):
		gc.getTeam(gc.getPlayer(0).getTeam()).setVassal(1, True, False)
		
		vassal = vassals()
		
		try:
			assertType(self, vassal, DefaultDict)
			self.assertEqual(vassal[0], [])
			self.assertEqual(vassal[1], [0])
		finally:
			gc.getTeam(gc.getPlayer(0).getTeam()).setVassal(1, False, False)
		
	def test_vassals_no_vassals(self):
		vassal = vassals()
		assertType(self, vassal, DefaultDict)
		self.assertEqual(vassal[0], [])
		self.assertEqual(vassal[1], [])


class TestMinor(TestCase):

	def test_is_minor_independent(self):
		self.assert_(is_minor(slot(iIndependent)))
		
	def test_is_minor_barbarian(self):
		self.assert_(is_minor(slot(iBarbarian)))
		
	def test_is_minor_player(self):
		self.assert_(is_minor(gc.getPlayer(slot(iIndependent))))
		
	def test_not_is_minor(self):
		self.assert_(not is_minor(0))
		

class TestEstimateDirection(TestCase):

	def test_estimate_directions(self):
		plot_directions = {
			(0, 1): DirectionTypes.DIRECTION_WEST,
			(1, 0): DirectionTypes.DIRECTION_SOUTH,
			(2, 1): DirectionTypes.DIRECTION_EAST,
			(1, 2): DirectionTypes.DIRECTION_NORTH,
		}
		
		for (x, y), direction in plot_directions.items():
			self.assertEqual(estimate_direction((1, 1), (x, y)), direction)
			
	def test_estimate_direction_plots(self):
		fromPlot = gc.getMap().plot(1, 1)
		toPlot = gc.getMap().plot(1, 0)
		self.assertEqual(estimate_direction(fromPlot, toPlot), DirectionTypes.DIRECTION_SOUTH)
		
	def test_estimate_direction_same(self):
		self.assertEqual(estimate_direction((0, 0), (0, 0)), DirectionTypes.NO_DIRECTION)


class TestYear(TestCase):

	def test_year(self):
		test_year = year(-3000)
		assertType(self, test_year, Turn)
		self.assertEqual(test_year, 0)
		
	def test_current_year(self):
		test_year = year()
		assertType(self, test_year, Turn)
		self.assertEqual(test_year, 0)
		

class TestMakeUnit(TestCase):

	def test_missionary(self):
		self.assertEqual(missionary(iJudaism), iJewishMissionary)
		
	def test_missionary_invalid(self):
		self.assertEqual(missionary(-1), None)
		
	def test_make_unit(self):
		unit = makeUnit(0, 4, (0, 0))
		assertType(self, unit, CyUnit)
		self.assertEqual(unit.getOwner(), 0)
		self.assertEqual(unit.getUnitType(), 4)
		self.assertEqual((unit.getX(), unit.getY()), (0, 0))
	
	def test_make_unit_plot(self):
		unit = makeUnit(0, 4, gc.getMap().plot(0, 0))
		assertType(self, unit, CyUnit)
		self.assertEqual(unit.getOwner(), 0)
		self.assertEqual(unit.getUnitType(), 4)
		self.assertEqual((unit.getX(), unit.getY()), (0, 0))
		
	def test_make_unit_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		unit = makeUnit(0, 4, city)
		
		try:
			assertType(self, unit, CyUnit)
			self.assertEqual(unit.getOwner(), 0)
			self.assertEqual(unit.getUnitType(), 4)
			self.assertEqual((unit.getX(), unit.getY()), (0, 0))
		finally:
			city.kill()
		
	def test_make_units(self):
		units = makeUnits(0, 4, (0, 0), 3)
		assertType(self, units, CreatedUnits)
		self.assertEqual(len(units), 3)
		for unit in units:
			self.assertEqual(unit.getOwner(), 0)
			self.assertEqual(unit.getUnitType(), 4)
			self.assertEqual((unit.getX(), unit.getY()), (0, 0))
			
			
class TestText(TestCase):

	def test_text(self):
		self.assertEqual(text("TXT_KEY_CIV_EGYPT_ADJECTIVE"), "Egyptian")
		
	def test_text_format(self):
		self.assertEqual(text("TXT_KEY_INTERFACE_CITY_CORE_POPULATION", 5), "Core Population: 5")
	
	def test_text_undefined(self):
		self.assertEqual(text("ABCDEF"), "ABCDEF")
		
	def test_text_if_exists(self):
		self.assertEqual(text_if_exists("TXT_KEY_CIV_EGYPT_ADJECTIVE"), "Egyptian")
		
	def test_text_if_exists_undefined(self):
		self.assertEqual(text_if_exists("ABDCDEF"), "")
		
	def test_text_if_exists_otherwise(self):
		self.assertEqual(text_if_exists("TXT_KEY_CIV_EGYPT_ADJECTIVE", otherwise="TXT_KEY_CIV_ENGLAND_ADJECTIVE"), "Egyptian")
		
	def test_text_if_exists_undefined_otherwise(self):
		self.assertEqual(text_if_exists("ABCDEF", otherwise="TXT_KEY_CIV_ENGLAND_ADJECTIVE"), "English")
		
	def test_text_if_exists_otherwise_format(self):
		self.assertEqual(text_if_exists("TXT_KEY_INTERFACE_CITY_CORE_POPULATION", 5, otherwise="TXT_KEY_CIV_ENGLAND_ADJECTIVE"), "Core Population: 5")
		
	def test_text_if_exists_undefined_otherwise_format(self):
		self.assertEqual(text_if_exists("ABDCDEF", 5, otherwise="TXT_KEY_INTERFACE_CITY_CORE_POPULATION"), "Core Population: 5")
		

class TestDistance(TestCase):

	def test_distance(self):
		self.assertEqual(distance((0, 0), (0, 2)), 2)
		self.assertEqual(real_distance((0, 0), (0, 2)), 2)
		
	def test_distance_plots(self):
		self.assertEqual(distance(gc.getMap().plot(0, 0), gc.getMap().plot(0, 2)), 2)
		self.assertEqual(real_distance(gc.getMap().plot(0, 0), gc.getMap().plot(0, 2)), 2)
		
	def test_distance_cities(self):
		city1 = gc.getPlayer(0).initCity(0, 0)
		city2 = gc.getPlayer(0).initCity(0, 2)
		
		try:
			self.assertEqual(distance(city1, city2), 2)
			self.assertEqual(real_distance(city1, city2), 2)
		finally:
			city1.kill()
			city2.kill()
		

class TestFind(TestCase):

	def setUp(self):
		self.numbers = [0, 4, 5, -1, 12, 3]

	def test_find_min(self):
		found = find_min(self.numbers)
		assertType(self, found, FindResult)
		self.assertEqual(found.result, -1)
		self.assertEqual(found.index, 3)
		self.assertEqual(found.value, -1)
		
	def test_find_max(self):
		found = find_max(self.numbers)
		assertType(self, found, FindResult)
		self.assertEqual(found.result, 12)
		self.assertEqual(found.index, 4)
		self.assertEqual(found.value, 12)
		
	def test_find_max_custom(self):
		found = find_max(self.numbers, lambda x: x % 3)
		assertType(self, found, FindResult)
		self.assertEqual(found.result, 5)
		self.assertEqual(found.index, 2)
		self.assertEqual(found.value, 2)
		
		
class TestRandom(TestCase):

	def run_random(self, random, min, max):
		bFoundMin = False
		bOutside = False
		for _ in range(10000):
			iRand = random()
			if iRand == min: bFoundMin = True
			if not min <= iRand < max: bOutside = True
		self.assert_(bFoundMin)
		self.assert_(not bOutside)
		
	def test_random(self):
		self.run_random(lambda: rand(10), 0, 10)
		
	def test_random_min(self):
		self.run_random(lambda: rand(10, 20), 10, 20)
		
	def test_random_entry(self):
		list = [0, 1, 2, 3, 4]
		self.assert_(random_entry(list) in list)
		
	def test_random_entry_empty(self):
		self.assertEqual(random_entry([]), None)
		

class TestNames(TestCase):

	def test_name(self):
		self.assertEqual(name(0), "Egypt")
		
	def test_name_player(self):
		self.assertEqual(name(gc.getPlayer(0)), "Egypt")
	
	def test_name_none(self):
		self.assertRaises(ValueError, name, None)
		
	def test_adjective(self):
		self.assertEqual(adjective(0), "Egyptian")
		
	def test_adjective_player(self):
		self.assertEqual(adjective(gc.getPlayer(0)), "Egyptian")
	
	def test_adjective_none(self):
		self.assertRaises(ValueError, adjective, None)
		
	def test_full_name(self):
		self.assertEqual(fullname(slot(iChina)), "Han Peoples")
		
	def test_full_name_player(self):
		self.assertEqual(fullname(player(iChina)), "Han Peoples")
	
	def test_full_name_none(self):
		self.assertRaises(ValueError, fullname, None)
		
		
class TestWrap(TestCase):

	def test_wrap_x(self):
		self.assertEqual(wrap(124, 0), (0, 0))
		
	def test_wrap_x_negative(self):
		self.assertEqual(wrap(-1, 0), (123, 0))
		
	def test_wrap_y(self):
		self.assertEqual(wrap(0, 68), (0, 67))
		
	def test_wrap_y_negative(self):
		self.assertEqual(wrap(0, -1), (0, 0))
		
	def test_wrap_noop(self):
		self.assertEqual(wrap(0, 0), (0, 0))
		
	def test_wrap_plots(self):
		self.assertEqual(wrap(gc.getMap().plot(0, 0)), (0, 0))
		
	def test_wrap_invalid_plot(self):
		self.assertEqual(wrap(gc.getMap().plot(124, 68)), None)
		
		
class TestLocation(TestCase):

	def base_test(self, expected_class, expected_value, func, *args):
		obj = func(*args)
		assertType(self, obj, expected_class)
		self.assertEqual((obj.getX(), obj.getY()), expected_value)


class TestPlot(TestLocation):

	def test_coords(self):
		self.base_test(CyPlot, (0, 0), plot, 0, 0)
		
	def test_tile(self):
		self.base_test(CyPlot, (0, 0), plot, (0, 0))
		
	def test_plot(self):
		self.base_test(CyPlot, (0, 0), plot, gc.getMap().plot(0, 0))
		
	def test_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		
		try:
			self.base_test(CyPlot, (0, 0), plot, city)
		finally:
			city.kill()
		
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		try:
			self.base_test(CyPlot, (0, 0), plot, unit)
		finally:
			unit.kill(False, 0)
		
	def test_invalid(self):
		self.assertRaises(TypeError, plot, 0, 0, 0)
		

class TestCity(TestLocation):

	def setUp(self):
		self.city = gc.getPlayer(0).initCity(0, 0)
		
	def tearDown(self):
		self.city.kill()
		
	def test_coords(self):
		self.base_test(CyCity, (0, 0), city, 0, 0)
		
	def test_tile(self):
		self.base_test(CyCity, (0, 0), city, (0, 0))
		
	def test_plot(self):
		self.base_test(CyCity, (0, 0), city, gc.getMap().plot(0, 0))
	
	def test_city(self):
		expected_city = self.city
		
		actual_city = city(self.city)
		
		assertType(self, actual_city, CyCity)
		self.assertEqual(actual_city, expected_city)
		
	def test_invalid(self):
		self.assertRaises(TypeError, city, 0, 0, 0)
		
	def test_no_city(self):
		self.assertEqual(city(0, 1), None)
		
	
class TestUnit(TestCase):
		
	def setUp(self):
		self.unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
	def tearDown(self):
		if self.unit.getX() >= 0:
			self.unit.kill(False, 0)
			
	def test_create_unit_key(self):
		key = UnitKey.of(self.unit)
		self.assertEqual(key.owner, self.unit.getOwner())
		self.assertEqual(key.id, self.unit.getID())
		
	def test_unit(self):
		u = unit(UnitKey.of(self.unit))
		self.assertEqual(u.getOwner(), self.unit.getOwner())
		self.assertEqual(u.getID(), self.unit.getID())
		
	def test_unit_invalid(self):
		self.assertRaises(TypeError, unit, self.unit)
		
		
class TestLocationFunction(TestCase):

	def test_plot(self):
		self.assertEqual(location(gc.getMap().plot(0, 0)), (0, 0))
		
	def test_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		
		try:
			self.assertEqual(location(city), (0, 0))
		finally:
			city.kill()
		
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		try:
			self.assertEqual(location(unit), (0, 0))
		finally:
			unit.kill(False, 0)
		
		
class TestTeam(TestCase):

	def test_current(self):
		self.assertEqual(team().getID(), 0)

	def test_team(self):
		t = gc.getTeam(0)
		self.assertEqual(team(t).getID(), t.getID())
		
	def test_player(self):
		p = gc.getPlayer(0)
		self.assertEqual(team(p).getID(), p.getTeam())
		
	def test_id(self):
		self.assertEqual(team(0).getID(), gc.getTeam(0).getID())
		
	def test_plot(self):
		plot = gc.getMap().plot(0, 0)
		plot.setOwner(0)
		
		try:
			self.assertEqual(team(plot).getID(), plot.getTeam())
		finally:
			plot.setOwner(-1)
		
	def test_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		
		try:
			self.assertEqual(team(city).getID(), city.getTeam())
		finally:
			city.kill()
		
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		try:
			self.assertEqual(team(unit).getID(), unit.getTeam())
		finally:
			unit.kill(False, 0)
		
	def test_invalid(self):
		self.assertRaises(TypeError, team, gc.getCivilizationInfo(0))
		
	def test_teamtype(self):
		self.assertEqual(teamtype(0).getID(), gc.getTeam(0).getID())
		

class TestPlayer(TestCase):

	def test_current(self):
		self.assertEqual(player().getID(), 0)

	def test_player(self):
		p = gc.getPlayer(0)
		self.assertEqual(player(p).getID(), p.getID())
	
	def test_civ(self):
		p = gc.getPlayer(0)
		self.assertEqual(player(iEgypt).getID(), p.getID())
		
	def test_team(self):
		t = gc.getTeam(0)
		self.assertEqual(player(t).getID(), t.getLeaderID())
		
	def test_id(self):
		self.assertEqual(player(0).getID(), gc.getPlayer(0).getID())
		
	def test_negative_id(self):
		self.assertEqual(player(-1), None)
		
	def test_plot(self):
		plot = gc.getMap().plot(0, 0)
		plot.setOwner(0)
		
		try:
			self.assertEqual(player(plot).getID(), plot.getOwner())
		finally:
			plot.setOwner(-1)
		
	def test_city(self):
		city = gc.getPlayer(0).initCity(0, 0)
		
		try:
			self.assertEqual(city.getOwner(), 0)
			self.assertEqual(player(city).getID(), city.getOwner())
		finally:
			city.kill()
		
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		try:
			self.assertEqual(player(unit).getID(), unit.getOwner())
		finally:
			unit.kill(False, 0)
		
	def test_invalid(self):
		self.assertRaises(TypeError, player, gc.getCivilizationInfo(0))
		
		
class TestCiv(TestCase):
	
	def test_id(self):
		self.assertEqual(civ(0), iEgypt)
		
	def test_player(self):
		self.assertEqual(civ(gc.getPlayer(0)), iEgypt)
		
	def test_team(self):
		self.assertEqual(civ(gc.getTeam(gc.getPlayer(0).getTeam())), iEgypt)
		
	def test_civ(self):
		self.assertEqual(civ(iEgypt), iEgypt)
	
	def test_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		try:
			self.assertEqual(civ(unit), iEgypt)
		finally:
			unit.kill(False, -1)
	
	def test_plot(self):
		plot = gc.getMap().plot(0, 0)
		plot.setOwner(0)
		
		try:
			self.assertEqual(civ(plot), iEgypt)
		finally:
			plot.setOwner(-1)
		
	def test_plot_unowned(self):
		plot = gc.getMap().plot(0, 0)
	
		self.assertEqual(civ(plot), NoCiv)
	
	def test_civ_none(self):
		self.assertEqual(civ(), iEgypt)
		
		
class TestActive(TestCase):

	def test_active(self):
		self.assertEqual(active(), gc.getGame().getActivePlayer())


class TestIterableHelpers(TestCase):

	def setUp(self):
		self.iterable = [1, 2, 3, 4, 5]
		
	def test_any_with_one(self):
		self.assert_(any([x >= 5 for x in self.iterable]))
		
	def test_any_with_all(self):
		self.assert_(any([x >= 1 for x in self.iterable]))
		
	def test_any_with_none(self):
		self.assert_(not any([x < 0 for x in self.iterable]))
		
	def test_all_with_one(self):
		self.assert_(not all([x >= 5 for x in self.iterable]))
		
	def test_all_with_all(self):
		self.assert_(all([x >= 1 for x in self.iterable]))
		
	def test_all_with_none(self):
		self.assert_(not all([x < 0 for x in self.iterable]))
	
	def test_none_with_one(self):
		self.assert_(not none([x >= 5 for x in self.iterable]))
		
	def test_none_with_all(self):
		self.assert_(not none([x >= 1 for x in self.iterable]))
	
	def test_none_with_none(self):
		self.assert_(none([x < 0 for x in self.iterable]))
		
	def test_next_once(self):
		first = next(self.iterable)
		self.assertEqual(first, 1)
		
	def test_next_twice(self):
		iterator = iter(self.iterable)
		first = next(iterator)
		second = next(iterator)
		self.assertEqual(first, 1)
		self.assertEqual(second, 2)
		
	def test_next_default(self):
		first = next([], -1)
		self.assertEqual(first, -1)
		
		
class TestClosestCity(TestCase):

	def test_closest_city(self):
		original_city = gc.getPlayer(0).initCity(63, 10)
		closest_city = gc.getPlayer(0).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(original_city)
		
		try:
			self.assertEqual((closest.getX(), closest.getY()), (closest_city.getX(), closest_city.getY()))
		finally:
			original_city.kill()
			closest_city.kill()
			farther_city.kill()
	
	def test_closest_unit(self):
		unit = gc.getPlayer(0).initUnit(4, 63, 10, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		closest_city = gc.getPlayer(0).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(unit)
		
		try:
			self.assertEqual((closest.getX(), closest.getY()), (closest_city.getX(), closest_city.getY()))
		finally:
			unit.kill(False, -1)
			closest_city.kill()
			farther_city.kill()
	
	def test_closest_owner(self):
		original_city = gc.getPlayer(0).initCity(63, 10)
		closest_city = gc.getPlayer(1).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(original_city, 0)
		
		try:
			self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		finally:
			original_city.kill()
			closest_city.kill()
			farther_city.kill()
	
	def test_closest_continents(self):
		original_city = gc.getPlayer(0).initCity(49, 35)
		closest_city = gc.getPlayer(0).initCity(47, 36)
		farther_city = gc.getPlayer(0).initCity(57, 27)
		
		closest = closestCity(original_city, same_continent=True)
		
		try:
			self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		finally:
			original_city.kill()
			closest_city.kill()
			farther_city.kill()
	
	def test_coastal(self):
		original_city = gc.getPlayer(0).initCity(63, 10)
		closest_city = gc.getPlayer(0).initCity(65, 11)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(original_city, coastal_only=True)
		
		try:
			self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		finally:
			original_city.kill()
			closest_city.kill()
			farther_city.kill()
	
	def test_no_result(self):
		original_city = gc.getPlayer(0).initCity(63, 10)
		
		closest = closestCity(original_city, owner=1)
		
		try:
			self.assert_(closest is None)
		finally:
			original_city.kill()
	
	def test_skip_city(self):
		unit = gc.getPlayer(0).initUnit(4, 63, 10, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		closest_city = gc.getPlayer(0).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest = closestCity(unit, skip_city=closest_city)
		
		try:
			self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		finally:
			unit.kill(False, -1)
			closest_city.kill()
			farther_city.kill()
	
	def test_skip_city_plot(self):
		unit = gc.getPlayer(0).initUnit(4, 63, 10, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		closest_city = gc.getPlayer(0).initCity(62, 13)
		farther_city = gc.getPlayer(0).initCity(61, 15)
		
		closest_city_plot = gc.getMap().plot(62, 13)
		
		closest = closestCity(unit, skip_city=closest_city_plot)
		
		try:
			self.assertEqual((closest.getX(), closest.getY()), (farther_city.getX(), farther_city.getY()))
		finally:
			unit.kill(False, -1)
			closest_city.kill()
			farther_city.kill()

class TestSpecialbuilding(TestCase):

	def test_temple(self):
		building = temple(iJudaism)
		
		self.assertEqual(building, iJewishTemple)
		
	def test_monastery(self):
		building = monastery(iIslam)
		
		self.assertEqual(building, iIslamicMonastery)
		
	def test_cathedral(self):
		building = cathedral(iBuddhism)
		
		self.assertEqual(building, iBuddhistCathedral)
	
	def test_shrine(self):
		building = shrine(iHinduism)
		
		self.assertEqual(building, iHinduShrine)


class TestMap(TestCase):

	def setUp(self):
		self.tiles = [[1, 2, 3],
					  [4, 5, 6],
					  [7, 8, 9]]
		self.map = Map(self.tiles)
	
	def test_init_no_list(self):
		self.assertRaises(ValueError, Map, 1)
	
	def test_init_not_empty(self):
		self.assertRaises(ValueError, Map, [])
	
	def test_init_different_widths(self):
		self.assertRaises(ValueError, Map, [[1], [2, 3]])
	
	def test_getitem(self):
		self.assertEqual(self.map[0, 0], 7)
		self.assertEqual(self.map[1, 0], 8)
		self.assertEqual(self.map[2, 0], 9)
		self.assertEqual(self.map[0, 1], 4)
		self.assertEqual(self.map[1, 1], 5)
		self.assertEqual(self.map[2, 1], 6)
		self.assertEqual(self.map[0, 2], 1)
		self.assertEqual(self.map[1, 2], 2)
		self.assertEqual(self.map[2, 2], 3)
		
	def test_setitem(self):
		self.map[1, 1] = 0
		self.assertEqual(self.map[1, 1], 0)
		
	def test_iter(self):
		expected_items = [((0, 0), 7), ((1, 0), 8), ((2, 0), 9), ((0, 1), 4), ((1, 1), 5), ((2, 1), 6), ((0, 2), 1), ((1, 2), 2), ((2, 2), 3)]
		actual_items = [item for item in self.map]
		
		self.assertEqual(set(actual_items), set(expected_items))
	
	def test_apply(self):
		otherMap = Map([[0, 0], [0, 0]])
		
		self.map.apply(otherMap)
		
		self.assertEqual(self.map[0, 0], 0)
		self.assertEqual(self.map[0, 1], 0)
		self.assertEqual(self.map[2, 2], 3)
		
	def test_apply_offset(self):
		otherMap = Map([[0, 0], [0, 0]])
		
		self.map.apply(otherMap, (1, 1))
		
		self.assertEqual(self.map[0, 0], 7)
		self.assertEqual(self.map[1, 1], 0)
		self.assertEqual(self.map[2, 2], 0)


class TestDeepList(TestCase):

	def test_list(self):
		result = deeplist([1, 2, 3])
		self.assertEqual(result, [1, 2, 3])
		
	def test_tuple(self):
		result = deeplist((1, 2, 3))
		self.assertEqual(result, [1, 2, 3])
		
	def test_deep_tuple(self):
		result = deeplist(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
		self.assertEqual(result, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])


class TestNullPlayer(TestCase):

	def setUp(self):
		self.null_player = NullPlayer()
		
	def test_is_player(self):
		self.assert_(isinstance(self.null_player, CyPlayer))
	
	def test_can_call(self):
		self.null_player.isAlive()
		self.null_player.randomMethodThatWouldNotExist()
		self.null_player.methodWithInput("string", 1, False)
		
	def test_can_chain(self):
		self.null_player.isAlive().isAlive()
		
	def test_evals_false(self):
		self.assert_(not self.null_player)
		
	def test_method_evals_false(self):
		self.assert_(not self.null_player.isAlive())
		
		
class TestNullTeam(TestCase):
	
	def setUp(self):
		self.null_team = NullTeam()
	
	def test_is_team(self):
		self.assert_(isinstance(self.null_team, CyTeam))
		
	def test_can_call(self):
		self.null_team.isAVassal()
		self.null_team.randomMethodThatWouldNotExist()
		self.null_team.methodWithInput("string", 1, False)
		
	def test_can_chain(self):
		self.null_team.isAVassal().isAVassal()
	
	def test_evals_false(self):
		self.assert_(not self.null_team)
		
	def test_method_evals_false(self):
		self.assert_(not self.null_team.isAVassal())


class TestPeriod(TestCase):

	def test_period(self):
		game.setPeriod(iEgypt, 123)
		iPeriod = period(iEgypt)
		
		try:
			self.assertEqual(iPeriod, 123)
		finally:
			game.setPeriod(iEgypt, -1)
	
	def test_period_not_set(self):
		iPeriod = period(iIran)
		self.assertEqual(iPeriod, -1)


class TestDivide(TestCase):

	def test_divide_one(self):
		players = Players([0, 1, 2])
		
		actual_divided = players.divide([100, 200, 300])
		
		self.assertEqual(len(actual_divided), 3)
		
		total_values = []
		for key, values in actual_divided:
			self.assert_(key in [100, 200, 300])
			self.assert_(isinstance(values, Players))
			self.assertEqual(len(values), 1)
			total_values += values
		
		self.assertEqual(set(total_values), set([0, 1, 2]))
		
	def test_divide_more(self):
		players = Players([0, 1, 2, 3, 4, 5])
		
		actual_divided = players.divide([100, 200, 300])
		
		self.assertEqual(len(actual_divided), 3)
		
		total_values = []
		for key, values in actual_divided:
			self.assert_(key in [100, 200, 300])
			self.assert_(isinstance(values, Players))
			self.assertEqual(len(values), 2)
			total_values += values
		
		self.assertEqual(set(total_values), set([0, 1, 2, 3, 4, 5]))
		
		
class TestFormatSeparators(TestCase):

	def test_format_one(self):
		list = [1]
		result = format_separators(list, ",", " and ")
		
		self.assertEqual(result, "1")
		
	def test_format_two(self):
		list = [1, 2]
		result = format_separators(list, ",", " and ")
		
		self.assertEqual(result, "1 and 2")
		
	def test_format_three(self):
		list = [1, 2, 3]
		result = format_separators(list, ",", " and ")
		
		self.assertEqual(result, "1, 2 and 3")
		
	def test_format_convert(self):
		list = [1, 2, 3]
		result = format_separators(list, ",", " and ", lambda x: x*x)
		
		self.assertEqual(result, "1, 4 and 9")


class TestSlot(TestCase):

	def test_slot(self):
		self.assertEqual(slot(iEgypt), 0)
		
	def test_slot_requires_civ(self):
		self.assertRaises(TypeError, slot, 0)
		
	def test_nonexistent(self):
		self.assertEqual(slot(iIran), -1)


class TestCivDict(TestCase):

	def setUp(self):
		self.civdict = CivDict({iEgypt: 0, iBabylonia: 1, iHarappa: 2})
		
	def test_is_dict(self):
		self.assert_(isinstance(self.civdict, dict))
		
	def test_get_civ(self):
		self.assertEqual(self.civdict[iEgypt], 0)
		
	def test_get_int(self):
		self.assertEqual(self.civdict[0], 0)
	
	def test_get_other(self):
		self.assertRaises(TypeError, self.civdict.__getitem__, 'string')
	
	def test_set_civ(self):
		tempdict = self.civdict.copy()
		tempdict[iChina] = 3
		self.assertEqual(tempdict[iChina], 3)
	
	def test_set_other(self):
		tempdict = self.civdict.copy()
		self.assertRaises(TypeError, tempdict.__setitem__, 3)
		
	def test_default_civ(self):
		tempdict = CivDict({}, -123)
		self.assertEqual(tempdict[iEgypt], -123)
		
	def test_default_int(self):
		tempdict = CivDict({}, -123)
		self.assertEqual(tempdict[0], -123)
		
	def test_contains_civ(self):
		self.assert_(iEgypt in self.civdict)
		
	def test_contains_int(self):
		self.assert_(0 in self.civdict)
	
	def test_contains_else_throws_error(self):
		self.assertRaises(TypeError, self.civdict.__contains__, 'string')
		

class TestSpread(TestCase):

	def test_spread_equal(self):
		elements = [1, 2, 3, 4]
		expected = [1, 2, 3, 4]
		
		actual = spread(elements, 4)
		
		self.assertEqual(actual, expected)
	
	def test_spread_double(self):
		elements = [1, 2, 3]
		expected = [1, None, 2, None, 3, None]
		
		actual = spread(elements, 6)
		
		self.assertEqual(actual, expected)
	
	def test_spread_more(self):
		elements = [1, 2, 3]
		expected = [1, None, 2, None, 3, None, None]
		
		actual = spread(elements, 7)
		
		self.assertEqual(actual, expected)
		
	def test_spread_another_more(self):
		elements = [1, 2, 3]
		expected = [1, None, 2, None, 3]
		
		actual = spread(elements, 5)
		
		self.assertEqual(actual, expected)
		
	def test_spread_half(self):
		elements = [1, 2, 3, 4, 5, 6]
		expected = [(1, 4), (2, 5), (3, 6)]
		
		actual = spread(elements, 3)
		
		self.assertEqual(actual, expected)
	
	def test_spread_third(self):
		elements = [1, 2, 3, 4, 5, 6]
		expected = [(1, 3, 5), (2, 4, 6)]
		
		actual = spread(elements, 2)
		
		self.assertEqual(actual, expected)
		
	def test_spread_less(self):
		elements = [1, 2, 3, 4, 5]
		expected = [(1, 3, 5), (2, 4)]
		
		actual = spread(elements, 2)
		
		self.assertEqual(actual, expected)
		
	def test_spread_double_offset(self):
		elements = [1, 2, 3]
		expected = [None, 1, None, 2, None, 3]
		
		actual = spread(elements, 6, offset=1)
		
		self.assertEqual(actual, expected)
	
	def test_spread_double_offset_2(self):
		elements = [1, 2, 3]
		expected = [3, None, 1, None, 2, None]
		
		actual = spread(elements, 6, offset=2)
		
		self.assertEqual(actual, expected)
	
	def test_spread_half_offset(self):
		elements = [1, 2, 3, 4, 5, 6]
		expected = [(3, 6), (1, 4), (2, 5)]
		
		actual = spread(elements, 3, offset=1)
		
		self.assertEqual(actual, expected)
	
	def test_spread_half_offset_2(self):
		elements = [1, 2, 3, 4, 5, 6]
		expected = [(2, 5), (3, 6), (1, 4)]
		
		actual = spread(elements, 3, offset=2)
		
		self.assertEqual(actual, expected)


class TestTechFactory(TestCase):

	def setUp(self):
		self.factory = TechFactory()

	def test_of(self):
		techs = self.factory.of(1, 2, 3)
		
		assertType(self, techs, TechCollection)
		self.assertEqual(techs.techs(), [1, 2, 3])
	
	def test_column(self):
		techs = self.factory.column(1)
		
		assertType(self, techs, TechCollection)
		self.assertEqual(techs.techs(), [i for i in range(7)])
	
	def test_era(self):
		techs = self.factory.era(0)
		
		assertType(self, techs, TechCollection)
		self.assertEqual(techs.techs(), [i for i in range(21)])


class TestTechCollection(TestCase):

	def setUp(self):
		self.techs = TechFactory().column(1)
	
	def test_including(self):
		techs = self.techs.including(7)
		
		assertType(self, techs, TechCollection)
		self.assertEqual(techs.techs(), [i for i in range(8)])
		
	def test_including_more(self):
		techs = self.techs.including(7, 8, 9)
		
		assertType(self, techs, TechCollection)
		self.assertEqual(techs.techs(), [i for i in range(10)])
	
	def test_without(self):
		techs = self.techs.without(6)
		
		assertType(self, techs, TechCollection)
		self.assertEqual(techs.techs(), [i for i in range(6)])
	
	def test_without_more(self):
		techs = self.techs.without(4, 5, 6)
		
		assertType(self, techs, TechCollection)
		self.assertEqual(techs.techs(), [i for i in range(4)])
	
	def test_iter(self):
		for i, tech in enumerate(self.techs):
			self.assertEqual(i, tech)


class TestMatching(TestCase):

	def setUp(self):
		self.even = lambda x: x % 2 == 0

	def test_true_one(self):
		result = matching(self.even, 2)
		
		self.assertEqual(result, 2)
		
	def test_false_one(self):
		result = matching(self.even, 1)
		
		self.assertEqual(result, None)
		
	def test_empty(self):
		result = matching(self.even)
		
		self.assertEqual(result, None)
	
	def test_true_first(self):
		result = matching(self.even, 2, 1, 3)
		
		self.assertEqual(result, 2)
	
	def test_true_second(self):
		result = matching(self.even, 1, 2, 3)
		
		self.assertEqual(result, 2)
		
	def test_true_none(self):
		result = matching(self.even, 1, 3, 5)
		
		self.assertEqual(result, None)


class TestDirection(TestCase):

	def test_cardinal(self):
		tile = direction((2, 2), DirectionTypes.DIRECTION_NORTH)
		
		self.assertEqual((tile.getX(), tile.getY()), (2, 3))
		
	def test_non_cardinal(self):
		tile = direction((2, 2), DirectionTypes.DIRECTION_NORTHEAST)
		
		self.assertEqual((tile.getX(), tile.getY()), (3, 3))
	
	def test_plot(self):
		plot = gc.getMap().plot(2, 2)
		tile = direction(plot, DirectionTypes.DIRECTION_NORTH)
		
		self.assertEqual((tile.getX(), tile.getY()), (2, 3))


class TestAt(TestCase):

	def test_same_tuples(self):
		result = at((0, 0), (0, 0))
		
		self.assertEqual(result, True)
	
	def test_different_tuples(self):
		result = at((0, 0), (0, 1))
		
		self.assertEqual(result, False)
		
	def test_same_plots(self):
		result = at(gc.getMap().plot(0, 0), gc.getMap().plot(0, 0))
		
		self.assertEqual(result, True)
		
	def test_different_plots(self):
		result = at(gc.getMap().plot(0, 0), gc.getMap().plot(0, 1))
		
		self.assertEqual(result, False)
	
	def test_same_mismatch(self):
		result = at(gc.getMap().plot(0, 0), (0, 0))
		
		self.assertEqual(result, True)
		
	def test_different_mismatch(self):
		result = at(gc.getMap().plot(0, 0), (0, 1))
		
		self.assertEqual(result, False)


class TestCapital(TestCase):

	def test_capital(self):
		city = gc.getPlayer(0).initCity(0, 0)
		
		capital_city = capital(0)
		
		try:
			self.assert_(capital_city is not None)
			self.assertEqual(city.getID(), capital_city.getID())
		finally:
			city.kill()
	
	def test_not_alive(self):
		capital_city = capital(1)
		
		self.assert_(capital_city is None)
	
	def test_minor(self):
		capital_city = capital(barbarian())
		
		self.assert_(capital_city is None)


class TestSign(TestCase):

	def test_positive(self):
		self.assertEqual(sign(100), 1)
		
	def test_negative(self):
		self.assertEqual(sign(-100), -1)
	
	def test_zero(self):
		self.assertEqual(sign(0), 0)


class TestTextProcessing(TestCase):

	def test_replace_first(self):
		text = "one two three four"
		result = replace_first(text, "TXT_KEY_CIV_EGYPT_ADJECTIVE")
		
		self.assertEqual(result, "Egyptian two three four")
	
	def test_replace_first_format(self):
		text = "one two three four"
		result = replace_first(text, "TXT_KEY_UHV_MORE_THAN", "ten eleven twelve")
		
		self.assertEqual(result, "more one than ten eleven twelve two three four")
	
	def test_shared_words(self):
		first_text = "one two three and some other text"
		second_text = "one two three there is different text here"
		
		result = shared_words([first_text, second_text])
		
		self.assertEqual(result, "one two three")
	
	def test_shared_words_substring(self):
		first_text = "one two three aaaaabc"
		second_text = "one two three aaaaabb"
		
		result = shared_words([first_text, second_text])
		
		self.assertEqual(result, "one two three")
	
	def test_replace_shared_words(self):
		first_text = "one two three and some other text"
		second_text = "one two three there is a different text here"
		
		first_result, second_result = replace_shared_words([first_text, second_text])
		
		self.assertEqual(first_result, "one two three and some other text")
		self.assertEqual(second_result, " there is a different text here")
		
	def test_replace_shared_words_three(self):
		first_text = "one two three and some other text"
		second_text = "one two three there is a different text here"
		third_text = "one two three yet another text or whatever"
		
		first_result, second_result, third_result = replace_shared_words([first_text, second_text, third_text])
		
		self.assertEqual(first_result, "one two three and some other text")
		self.assertEqual(second_result, " there is a different text here")
		self.assertEqual(third_result, " yet another text or whatever")
	
	def test_replace_shared_words_minimal(self):
		first_text = "one two three and some other text"
		second_text = "one two three and different text"
		third_text = "one two three this is different"
		
		first_result, second_result, third_result = replace_shared_words([first_text, second_text, third_text])
		
		self.assertEqual(first_result, "one two three and some other text")
		self.assertEqual(second_result, " and different text")
		self.assertEqual(third_result, " this is different")
	
	def test_capitalize(self):
		text = "word"
		result = capitalize(text)
		
		self.assertEqual(result, "Word")
	
	def test_capitalize_empty(self):
		text = ""
		result = capitalize(text)
		
		self.assertEqual(result, "")
	
	def test_capitalize_already_capital(self):
		text = "Word"
		result = capitalize(text)
		
		self.assertEqual(result, "Word")
	
	def test_capitalize_multiple_words(self):
		text = "some word"
		result = capitalize(text)
		
		self.assertEqual(result, "Some word")
	
	def test_number_word_a(self):
		result = number_word(1)
		
		self.assertEqual(result, "a")
	
	def test_number_word_two(self):
		result = number_word(2)
		
		self.assertEqual(result, "two")
	
	def test_number_word_ten(self):
		result = number_word(10)
		
		self.assertEqual(result, "ten")
	
	def test_number_word_twenty(self):
		result = number_word(20)
		
		self.assertEqual(result, "20")
	
	def test_ordinal_word_first(self):
		self.assertEqual(ordinal_word(1), "first")
	
	def test_ordinal_word_100th(self):
		self.assertEqual(ordinal_word(100), "100th")
	
	def test_plural(self):
		result = plural("word")
		
		self.assertEqual(result, "words")
	
	def test_plural_ends_with_s(self):
		result = plural("words")
		
		self.assertEqual(result, "words")
	
	def test_plural_ends_with_y(self):
		result = plural("library")
		
		self.assertEqual(result, "libraries")
	
	def test_plural_ends_with_ch(self):
		self.assertEqual(plural("church"), "churches")
	
	def test_plural_ends_with_sh(self):
		self.assertEqual(plural("marsh"), "marshes")
	
	def test_plural_ends_with_man(self):
		self.assertEqual(plural("swordsman"), "swordsmen")
	
	def test_plural_irregular(self):
		self.assertEqual(plural("Ship of the Line"), "Ships of the Line")
		self.assertEqual(plural("Great Statesman"), "Great Statesmen")
		self.assertEqual(plural("cathedral of your state religion"), "cathedrals of your state religion")
	
	def test_format_date_positive(self):
		self.assertEqual(format_date(1000), "1000 AD")
	
	def test_format_date_negative(self):
		self.assertEqual(format_date(-500), "500 BC")
	

class TestConcat(TestCase):

	def test_listify_list(self):
		self.assertEqual(listify([1, 2, 3]), [1, 2, 3])
	
	def test_listify_tuple(self):
		self.assertEqual(listify((1, 2, 3)), [1, 2, 3])
	
	def test_listify_set(self):
		self.assertEqual(listify(set([1, 2, 3])), [1, 2, 3])
	
	def test_listify_generator(self):
		self.assertEqual(listify(i for i in xrange(3)), [0, 1, 2])
	
	def test_listify_int(self):
		self.assertEqual(listify(1), [1])
	
	def test_listify_none(self):
		self.assertEqual(listify(None), [])
	
	def test_concat_lists(self):
		self.assertEqual(concat([1, 2], [3, 4]), [1, 2, 3, 4])
	
	def test_concat_list_and_int(self):
		self.assertEqual(concat([1, 2], 3), [1, 2, 3])
	
	def test_concat_int_and_list(self):
		self.assertEqual(concat(1, [2, 3]), [1, 2, 3])
	
	def test_concat_int_and_int(self):
		self.assertEqual(concat(1, 2), [1, 2])
	
	def test_concat_generator_and_list(self):
		self.assertEqual(concat((i for i in xrange(2)), 2), [0, 1, 2])
	
	def test_concat_more_than_two(self):
		self.assertEqual(concat([1, 2], 3, (4, 5)), [1, 2, 3, 4, 5])
	
	def test_concat_with_none(self):
		self.assertEqual(concat([1, 2], None), [1, 2])


class TestFuncWrappers(TestCase):

	def test_equals(self):
		def func(x, y):
			return x + y
		
		equals_func = equals(func)
		
		self.assertEqual(equals_func(1, 2, 3), True)
		self.assertEqual(equals_func(1, 2, 4), False)
	
	def test_positive(self):
		def func(x, y):
			return x + y
		
		positive_func = positive(func)
		
		self.assertEqual(positive_func(1, 1), True)
		self.assertEqual(positive_func(0, 0), False)
		self.assertEqual(positive_func(1, -2), False)


class TestAverage(TestCase):

	def test_average(self):
		def count(list):
			return len(list)
		
		def value(list):
			return sum(list)
		
		average_func = average(value, count)
		
		self.assertEqual(average_func([1, 2, 3]), 2.0)
		self.assertEqual(average_func([]), 0.0)


class TestCount(TestCase):

	def test_count(self):
		self.assertEqual(count([1, 2, 3, 4, 5]), 5)
	
	def test_count_condition(self):
		self.assertEqual(count([1, 2, 3, 4, 5], lambda x: x >= 3), 3)


class TestLazyPlots(TestCase):

	def setUp(self):
		self.factory = LazyPlotFactory()

	def test_capital_none(self):
		capital = self.factory.capital(0)
		
		assertType(self, capital, LazyPlots)
		
		self.assertEqual(capital.count(), 0)
	
	def test_capital_before(self):
		city = gc.getPlayer(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(city.isCapital(), True)
		
			capital = self.factory.capital(0)
		
			assertType(self, capital, LazyPlots)
		
			self.assertEqual(capital.count(), 1)
			self.assertEqual(capital.first().getX(), 61)
			self.assertEqual(capital.first().getY(), 31)
		finally:
			city.kill()
	
	def test_capital_after(self):
		capital = self.factory.capital(0)
		
		assertType(self, capital, LazyPlots)
		
		city = gc.getPlayer(0).initCity(61, 31)
		city.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(city.isCapital(), True)
		
			self.assertEqual(capital.count(), 1)
			self.assertEqual(capital.first().getX(), 61)
			self.assertEqual(capital.first().getY(), 31)
		finally:
			city.kill()
	
	def test_capital_changed(self):
		capital = self.factory.capital(0)
		
		city1 = gc.getPlayer(0).initCity(61, 31)
		city1.setHasRealBuilding(iPalace, True)
		
		try:
			self.assertEqual(city1.isCapital(), True)
		
			self.assertEqual(capital.count(), 1)
			self.assertEqual(capital.first().getX(), 61)
			self.assertEqual(capital.first().getY(), 31)
		
			city2 = gc.getPlayer(0).initCity(63, 31)
			city2.setHasRealBuilding(iPalace, True)
		
			try:
				self.assertEqual(city2.isCapital(), True)
		
				self.assertEqual(capital.count(), 1)
				self.assertEqual(capital.first().getX(), 63)
				self.assertEqual(capital.first().getY(), 31)
			finally:
				city2.kill()
		finally:
			city1.kill()
	
	def test_normal(self):
		normal = self.factory.normal(0)
		
		self.assertEqual(normal.unique(), plots.normal(0).unique())


class TestVariadic(TestCase):

	def test_list(self):
		self.assertEqual(variadic([1, 2, 3]), [1, 2, 3])
	
	def test_tuple(self):
		self.assertEqual(variadic((1, 2, 3)), [1, 2, 3])
	
	def test_varargs(self):
		self.assertEqual(variadic(1, 2, 3), [1, 2, 3])
	
	def test_set(self):
		self.assertEqual(variadic(set([1, 2, 3])), [1, 2, 3])
	
	def test_item(self):
		self.assertEqual(variadic(1), [1])
	
	def test_empty(self):
		self.assertEqual(variadic(), [])
	
	def test_generator(self):
		result = variadic(i for i in xrange(3))
	
		self.assertEqual(isinstance(result, types.GeneratorType), True)
		self.assertEqual([x for x in result], [0, 1, 2])


class TestMetrics(TestCase):

	def test_metrics(self):
		metric1 = lambda x, y: x+y
		metric2 = lambda x, y: x*y
		metric3 = lambda x, y: x >= y and x or y
		
		combined = metrics(metric1, metric2, metric3)
		
		self.assertEqual(combined(1, 2), (3, 2, 2))
		self.assertEqual(combined(3, 3), (6, 9, 3))
		self.assertEqual(combined(10, 9), (19, 90, 10))
	
	def test_bool_metric(self):
		metric = lambda x: x >= 10
		result = bool_metric(metric)
		
		self.assertEqual(result(0), 0)
		self.assertEqual(result(10), 1)
		self.assertEqual(result(20), 1)
	
	def test_bool_metric_additional_arguments(self):
		metric = lambda x, y: x >= y
		result = bool_metric(metric, 10)
		
		self.assertEqual(result(0), 0)
		self.assertEqual(result(10), 1)
		self.assertEqual(result(20), 1)


class TestDuplefy(TestCase):

	def test_duple(self):
		self.assertEqual(duplefy(1, 2), (1, 2))
	
	def test_single(self):
		self.assertEqual(duplefy(1), 1)
	
	def test_none(self):
		self.assertRaises(Exception, duplefy)
	
	def test_more(self):
		self.assertRaises(Exception, duplefy, 1, 2, 3)


class TestDeferredCollection(TestCase):

	def test_deferred(self):
		even = lambda p: (p.getX() + p.getY()) % 2 == 0
	
		deferred = DeferredCollectionFactory.plots()
		deferred = deferred.rectangle((0, 0), (1, 1))
		deferred = deferred.where(even)
		
		assertType(self, deferred, DeferredCollection)
		self.assertEqual(deferred.calls, [('rectangle', ((0, 0), (1, 1))), ('where', (even,))])
		
		collection = deferred.create()
		
		assertType(self, collection, Plots)
		self.assertEqual(len(collection), 2)
		self.assertEqual((0, 0) in collection, True)
		self.assertEqual((1, 1) in collection, True)
	
	def test_deferred_named(self):
		deferred = DeferredCollectionFactory.plots()
		deferred = deferred.all()
		deferred = deferred.clear_named("abcd")
		
		self.assertEqual(deferred.name(), "abcd")
		
		collection = deferred.create()
		
		assertType(self, collection, Plots)
		self.assertEqual(collection.name(), "abcd")
	
	def test_deferred_named_from_civ(self):
		deferred = DeferredCollectionFactory.plots()
		deferred = deferred.normal(iRome)
		
		self.assertEqual(deferred.name(), "Rome")
		
		collection = deferred.create()
		
		self.assertEqual(collection.name(), "Rome")
	
	def test_deferred_multiple_creates(self):
		deferred = DeferredCollectionFactory.plots()
		deferred = deferred.rectangle((0, 0), (1, 1))
		
		col1 = deferred.create()
		col2 = deferred.create()
		
		self.assertEqual(id(col1) != id(col2), True)
	
	def test_deferred_iter(self):
		deferred = DeferredCollectionFactory.plots()
		deferred = deferred.rectangle((0, 0), (1, 1))
		
		assertType(self, deferred, DeferredCollection)
		
		iterated = set([(plot.getX(), plot.getY()) for plot in deferred])
		
		assertType(self, deferred, DeferredCollection)
		self.assertEqual(iterated, set([(0, 0), (0, 1), (1, 0), (1, 1)]))
	
	def test_deferred_add(self):
		deferred1 = DeferredCollectionFactory.plots().rectangle((0, 0), (1, 1))
		deferred2 = DeferredCollectionFactory.plots().rectangle((2, 0), (3, 1))
		
		assertType(self, deferred1, DeferredCollection)
		assertType(self, deferred2, DeferredCollection)
		
		deferred = deferred1 + deferred2
		
		assertType(self, deferred, CombinedDeferredCollection)
		
		collection = deferred.create()
		
		assertType(self, collection, Plots)
		self.assertEqual(len(collection), 8)


class TestUnique(TestCase):

	def test_unique_list(self):
		self.assertEqual(unique([1, 1, 1, 2, 2, 3]), [1, 2, 3])
	
	def test_unique_generator(self):
		self.assertEqual(unique(int(i/2) for i in range(6)), [0, 1, 2])
	
	def test_unique_tuple(self):
		self.assertEqual(unique((1, 1, 1, 2, 2, 3)), [1, 2, 3])


class TestChunks(TestCase):

	def test_equal(self):
		self.assertEqual(chunks([1, 2, 3], 3), [[1, 2, 3]])
	
	def test_one(self):
		self.assertEqual(chunks([1, 2, 3], 1), [[1], [2], [3]])
	
	def test_multiple(self):
		self.assertEqual(chunks([1, 2, 3, 4, 5, 6], 3), [[1, 2, 3], [4, 5, 6]])
	
	def test_remainder(self):
		self.assertEqual(chunks([1, 2, 3, 4, 5], 3), [[1, 2, 3], [4, 5]])


class TestMission(TestCase):

	def setUp(self):
		self.unit = gc.getPlayer(0).initUnit(0, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
	def tearDown(self):
		self.unit.kill(False, -1)

	def test_mission_only(self):
		mission(self.unit, MissionTypes.MISSION_SLEEP, bAppend=True)
		
		self.assertEqual(self.unit.getGroup().getMissionType(0), MissionTypes.MISSION_SLEEP)
		self.assertEqual(self.unit.getGroup().getMissionData1(0), -1)
		self.assertEqual(self.unit.getGroup().getMissionData2(0), -1)
	
	def test_mission_with_data(self):
		mission(self.unit, MissionTypes.MISSION_SLEEP, data=(1, 2), bAppend=True)
		
		self.assertEqual(self.unit.getGroup().getMissionType(0), MissionTypes.MISSION_SLEEP)
		self.assertEqual(self.unit.getGroup().getMissionData1(0), 1)
		self.assertEqual(self.unit.getGroup().getMissionData2(0), 2)
	
	def test_mission_with_data_none(self):
		mission(self.unit, MissionTypes.MISSION_SLEEP, data=None, bAppend=True)
		
		self.assertEqual(self.unit.getGroup().getMissionType(0), MissionTypes.MISSION_SLEEP)
		self.assertEqual(self.unit.getGroup().getMissionData1(0), -1)
		self.assertEqual(self.unit.getGroup().getMissionData2(0), -1)
	
	def test_mission_with_data_one(self):
		mission(self.unit, MissionTypes.MISSION_SLEEP, data=1, bAppend=True)
		
		self.assertEqual(self.unit.getGroup().getMissionType(0), MissionTypes.MISSION_SLEEP)
		self.assertEqual(self.unit.getGroup().getMissionData1(0), 1)
		self.assertEqual(self.unit.getGroup().getMissionData2(0), -1)


class TestGetArea(TestCase):

	def setUp(self):
		self.africaTile = (48, 30)
		self.americaTile = (37, 28)
		
		self.africaID = plot(self.africaTile).getArea()
		self.americaID = plot(self.americaTile).getArea()
		
	def test_id(self):
		self.assertEqual(getArea(self.africaID), self.africaID)
		self.assertEqual(getArea(self.americaID), self.americaID)
	
	def test_tile(self):
		self.assertEqual(getArea(self.africaTile), self.africaID)
		self.assertEqual(getArea(self.americaTile), self.americaID)
	
	def test_plot(self):
		self.assertEqual(getArea(plot(self.africaTile)), self.africaID)
		self.assertEqual(getArea(plot(self.americaTile)), self.americaID)
	
	def test_city(self):
		africaCity = gc.getPlayer(0).initCity(*self.africaTile)
		americaCity = gc.getPlayer(0).initCity(*self.americaTile)
		
		try:
			self.assertEqual(getArea(africaCity), self.africaID)
			self.assertEqual(getArea(americaCity), self.americaID)
		finally:
			africaCity.kill()
			americaCity.kill()


class TestCivFactory(TestCase):

	def setUp(self):
		self.factory = CivFactory()

	def test_of_one(self):
		civs = self.factory.of(iEgypt)
		
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), 1)
		
		assertType(self, civs[0], Civ)
		self.assertEqual(civs[0], iEgypt)
	
	def test_of_more(self):
		civs = self.factory.of(iEgypt, iBabylonia, iHarappa)
		
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), 3)
		
		for i, iCiv in enumerate([iEgypt, iBabylonia, iHarappa]):
			assertType(self, civs[i], Civ)
			self.assertEqual(civs[i], iCiv)
	
	def test_of_none(self):
		civs = self.factory.of()
		
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), 0)
	
	def test_of_int(self):
		civs = self.factory.of(0)
		
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), 1)
		
		assertType(self, civs[0], Civ)
		self.assertEqual(civs[0], iEgypt)


class TestDictMax(TestCase):

	def test_dict_max(self):
		dict = {
			1: 100,
			2: 200,
			3: 300,
		}
		
		self.assertEqual(dict_max(dict), 3)
	
	def test_dict_max_tie(self):
		dict = {
			1: 100,
			2: 200,
			3: 200,
		}
		
		self.assertEqual(dict_max(dict), 2)
	
	def test_dict_max_empty(self):
		self.assertEqual(dict_max({}), None)


class TestCivFactory(TestCase):

	def setUp(self):
		self.factory = CivFactory()

	def test_all(self):
		civs = self.factory.all()
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), iNumCivs)
		
	def test_major(self):
		civs = self.factory.major()
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), len(lBirthOrder))
		
	def test_of_civs(self):
		expected_civs = [iEgypt, iBabylonia, iHarappa]
		actual_civs = self.factory.of(iEgypt, iBabylonia, iHarappa)
		
		assertType(self, actual_civs, Civilizations)
		self.assertEqual(len(actual_civs), 3)
		
		for iCiv in expected_civs:
			self.assertEqual(iCiv in actual_civs, True)
	
	def test_of_players(self):
		expected_civs = [iEgypt, iBabylonia, iHarappa]
		actual_civs = self.factory.of(0, 1, 2)
		
		assertType(self, actual_civs, Civilizations)
		self.assertEqual(len(actual_civs), 3)
		
		for iCiv in expected_civs:
			self.assertEqual(iCiv in actual_civs, True)


class TestCivilizations(TestCase):

	def setUp(self):
		self.civs = Civilizations([iEgypt, iBabylonia, iHarappa])

	def test_contains_player(self):
		self.assertEqual(gc.getPlayer(0) in self.civs, True)
	
	def test_contains_player_id(self):
		self.assertEqual(0 in self.civs, True)
		
	def test_contains_civ_id(self):
		self.assertEqual(iEgypt in self.civs, True)
		
	def test_iterate(self):
		for item in self.civs:
			self.assertEqual(isinstance(item, Civ), True)
			
	def test_string(self):
		expected_names = "The Egyptians,The Babylonians,The Harappans"
		actual_names = str(self.civs)
		self.assertEqual(actual_names, expected_names)
	
	def test_without_civ_id(self):
		civs = self.civs.without(iEgypt)
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), 2)
		self.assertEqual(iEgypt not in civs, True)
		
	def test_without_player_id(self):
		civs = self.civs.without(0)
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), 2)
		self.assertEqual(iEgypt not in civs, True)
		
	def test_without_list(self):
		civs = self.civs.without([iEgypt, iBabylonia])
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), 1)
		self.assertEqual(iHarappa in civs, True)
		
	def test_without_set(self):
		civs = self.civs.without(set([iEgypt, iBabylonia]))
		assertType(self, civs, Civilizations)
		self.assertEqual(len(civs), 1)
		self.assertEqual(iHarappa in civs, True)
		
	def test_can_be_built_from_players(self):
		civs = Civilizations([0, 1])
		
		self.assertEqual(iEgypt in civs, True)
		self.assertEqual(iBabylonia in civs, True)


class TestSignature(TestCase):

	def test_without_args(self):
		def some_function():
			pass
		
		self.assertEqual(signature(some_function), "some_function()")
	
	def test_with_args(self):
		def some_function(arg1, arg2, arg3):
			pass
		
		self.assertEqual(signature(some_function, 1, "2", None), "some_function(1, 2, None)")
	
	def test_with_kwargs(self):
		def some_function(arg1, arg2, arg3):
			pass
		
		self.assertEqual(signature(some_function, arg1=1, arg2="2", arg3=None), "some_function(arg1=1, arg2=2, arg3=None)")
	
	def test_with_default_kwargs(self):
		def some_function(arg1=1, arg2="2", arg3=None):
			pass
		
		self.assertEqual(signature(some_function), "some_function()")
	
	def test_with_generic_args(self):
		def some_function(*args):
			pass
		
		self.assertEqual(signature(some_function, 1, "2", None), "some_function(1, 2, None)")
	
	def test_with_generic_kwargs(self):
		def some_function(**kwargs):
			pass
		
		self.assertEqual(signature(some_function, arg1=1, arg2="2", arg3=None), "some_function(arg1=1, arg2=2, arg3=None)")
	
	def test_combined(self):
		def some_function(*args, **kwargs):
			pass
		
		self.assertEqual(signature(some_function, 1, "2", None, arg4=4, arg5="5", arg6=None), "some_function(1, 2, None, arg4=4, arg5=5, arg6=None)")
	

test_cases = [
	TestTurn, 
	TestInfos, 
	TestDefaultDict, 
	TestCreatedUnits, 
	TestPlayers, 
	TestPlayerFactory,
	TestUnits,
	TestUnitFactory,
	TestPlots,
	TestPlotFactory,
	TestCities,
	TestCityFactory,
	TestMove,
	TestHasCivic,
	TestScenarioUtils,
	TestUniqueUnitsAndBuildings,
	TestMasterAndVassal,
	TestMinor,
	TestEstimateDirection,
	TestYear,
	TestMakeUnit,
	TestText,
	TestFind,
	TestRandom,
	TestNames,
	TestWrap,
	TestPlot,
	TestCity,
	TestUnit,
	TestLocationFunction,
	TestTeam,
	TestPlayer,
	TestCiv,
	TestActive,
	TestIterableHelpers,
	TestClosestCity,
	TestSpecialbuilding,
	TestMap,
	TestDeepList,
	TestNullPlayer,
	TestNullTeam,
	TestPeriod,
	TestDivide,
	TestFormatSeparators,
	TestSlot,
	TestCivDict,
	TestSpread,
	TestTechFactory,
	TestTechCollection,
	TestMatching,
	TestDirection,
	TestAt,
	TestCapital,
	TestSign,
	TestTextProcessing,
	TestConcat,
	TestFuncWrappers,
	TestAverage,
	TestCount,
	TestLazyPlots,
	TestVariadic,
	TestMetrics,
	TestDuplefy,
	TestDeferredCollection,
	TestUnique,
	TestChunks,
	TestMission,
	TestGetArea,
	TestCivFactory,
	TestDictMax,
	TestCivFactory,
	TestCivilizations,
	TestSignature
]


setup()
		
suite = TestSuite([makeSuite(case) for case in test_cases])
TextTestRunner(verbosity=2).run(suite)

gc.getPlayer(0).initUnit(0, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)