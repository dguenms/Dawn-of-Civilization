from Core import *
from VictoryArguments import *
from VictoryUtils import *


class Enum(object):

	@staticmethod
	def of(type, names):
		return (Enum(type, iValue, name) for iValue, name in enumerate(names))

	def __init__(self, type, iValue, name):
		self.iValue = iValue
		
		self.type = type
		self.name = name
	
	def __repr__(self):
		return "%s.%s" % (self.type, self.name)
		
	def __eq__(self, other):
		if not isinstance(other, Enum):
			return False
		
		return (self.type, self.iValue) == (other.type, other.iValue)


class Type(object):

	def __init__(self, name):
		self.name = name
	
	def __repr__(self):
		return self.name
	
	def __eq__(self, other):
		return type(self) == type(other)
		
	def validate(self, argument):
		if isinstance(argument, Aggregate):
			return argument.validate(self.validate_func)
		return self.validate_func(argument)
	
	def format(self, argument, **options):
		if isinstance(argument, Aggregate):
			return argument.format(self.format_func, **options)
		if isinstance(argument, NamedArgument):
			return argument.name()
		return self.format_func(argument, **options)
		
	def area(self, argument):
		return None
	
	def scale(self, argument):
		return argument
	
	def format_repr(self, argument):
		if isinstance(argument, Aggregate):
			return argument.format(self.format_repr_func)
		if isinstance(argument, NamedArgument):
			return argument.name()
		return self.format_repr_func(argument)
		
	def validate_func(self, argument):
		raise NotImplementedError()
	
	def format_func(self, argument, **options):
		raise NotImplementedError()
	
	def format_repr_func(self, argument):
		return self.format_func(argument)


class SimpleType(Type):

	def __init__(self, name, type):
		Type.__init__(self, name)
		
		self.type = type
	
	def validate_func(self, argument):
		return isinstance(argument, self.type)
		
	def format_func(self, argument, **options):
		return str(argument)


class InfoType(Type):

	def __init__(self, name, info):
		Type.__init__(self, name)
		
		self.info = info
	
	def __eq__(self, other):
		if not isinstance(other, InfoType):
			return False
		
		return type(self.info) == type(other.info)
		
	def validate_func(self, argument):
		return isinstance(argument, (DeferredArgument, int))
	
	def format_func(self, argument, bPlural=False, **options):
		text = self.info(argument).getText()
		if bPlural:
			text = plural(text)
		return format_articles(text)
	
	def format_repr_func(self, argument, bPlural=False, **options):
		return capitalize(self.format_func(argument, bPlural=bPlural, **options))


class InfosType(Type):

	def __init__(self, name, info):
		Type.__init__(self, name)
		
		self.sub_type = InfoType(name, info)
	
	def validate_func(self, argument):
		if isinstance(argument, NamedList):
			return True
	
		if isinstance(argument, list) and all(self.sub_type.validate(entry) for entry in argument):
			return True
		
		return False
	
	def format_func(self, argument):
		if isinstance(argument, InfoCollection):
			if argument.name():
				return argument.name()
	
		return format_separators(argument, ",", text("TXT_KEY_OR"), self.sub_type.format)


class AmountType(Type):

	def scale(self, argument):
		return scale(argument)

	def validate_func(self, argument):
		return isinstance(argument, int)
	
	def format_func(self, argument, **options):
		return str(argument)
		
		
class CountType(Type):
	
	def validate_func(self, argument):
		return isinstance(argument, int)
	
	def format_func(self, argument, **options):
		return number_word(argument)
	
	def format_repr_func(self, argument):
		return str(argument)


class TurnsType(CountType):

	def scale(self, argument):
		return scale(argument)


class AreaType(Type):

	def validate_func(self, argument):
		return isinstance(argument, AreaArgument)
	
	def format_func(self, argument, **options):
		return argument.name()
		
	def area(self, argument):
		if isinstance(argument, Aggregate):
			return sum([argument_item.create() for argument_item in argument.items], plots.none())
		
		return argument.create()


class PercentageType(Type):

	def validate_func(self, argument):
		return isinstance(argument, int)
	
	def format_func(self, argument, **options):
		if argument == 50:
			return text("TXT_KEY_VICTORY_HALF")
	
		return "%d%%" % argument
	
	def format_repr_func(self, argument, **options):
		return "%d%%" % argument


class CityType(Type):

	def validate_func(self, argument):
		return isinstance(argument, CityArgument)
	
	def format_func(self, argument, **options):
		return argument.name()
	
	def area(self, argument):
		return argument.area()


class CivsType(Type):

	def validate_func(self, argument):
		return isinstance(argument, CivsArgument)
	
	def format_func(self, argument):
		return argument.name()


class ReligionAdjectiveType(InfoType):

	def __init__(self, name):
		InfoType.__init__(self, name, infos.religion)
	
	def format_func(self, argument, bPlural=False, **options):
		return text(infos.religion(argument).getAdjectiveKey())
	
	def format_repr_func(self, argument):
		return infos.religion(argument).getText()


class CultureLevelType(Type):

	def validate_func(self, argument):
		return isinstance(argument, int)
	
	def format_func(self, argument):
		return infos.cultureLevel(argument).getText().lower()
	
	def format_repr_func(self, argument):
		return infos.cultureLevel(argument).getText()


class AttitudeType(Type):

	def validate_func(self, argument):
		return isinstance(argument, AttitudeTypes)
	
	def format_func(self, argument):
		return infos.attitude(argument).getDescription().lower()
	
	def format_repr_func(self, argument):
		return infos.attitude(argument).getDescription()


class UnitCombatType(Type):

	def validate_func(self, argument):
		return isinstance(argument, UnitCombatTypes)
	
	def format_func(self, argument):
		return infos.unitCombat(argument).getDescription().lower()
	
	def format_repr_func(self, argument):
		return infos.unitCombat(argument).getDescription().split(" ")[0]


class AreaOrCityType(Type):

	def validate_func(self, argument):
		return isinstance(argument, (AreaArgument, CityArgument))
	
	def format_func(self, argument):
		return argument.name()
	
	def area(self, argument):
		if isinstance(argument, AreaArgument):
			return argument.create()
		if isinstance(argument, CityArgument):
			return argument.area()


class SpecialistType(InfoType):

	def __init__(self, name):
		InfoType.__init__(self, name, infos.specialist)
	
	def format_great_specialist_short(self, iSpecialist, **options):
		return self.format_func(iSpecialist, **options).split(" ")[1]
	
	def format(self, argument, **options):
		if isinstance(argument, Aggregate) and not argument.name():
			if all(iSpecialist in lGreatSpecialists for iSpecialist in argument.items):
				formatted = argument.format(self.format_great_specialist_short, **options)
				return self.format_func(lGreatSpecialists[0]).split(" ")[0] + " " + formatted
		
		return InfoType.format(self, argument, **options)


class ResourceType(InfoType):

	def __init__(self, name):
		InfoType.__init__(self, name, infos.bonus)
	
	def format_func(self, argument, **options):
		formatted = InfoType.format_func(self, argument, **options)
		if formatted[-1] == "s":
			formatted = formatted[:-1]
		return formatted


AMOUNT = AmountType("Amount")
AREA = AreaType("Area")
AREA_OR_CITY = AreaOrCityType("AreaOrCity")
ATTITUDE = AttitudeType("Attitude")
BUILDING = InfoType("Building", infos.building)
CITY = CityType("City")
CIVS = CivsType("Civs")
CORPORATION = InfoType("Corporation", infos.corporation)
COUNT = CountType("Count")
CULTURELEVEL = CultureLevelType("CultureLevel")
ERA = InfoType("Era", infos.era)
FEATURE = InfoType("Feature", infos.feature)
IMPROVEMENT = InfoType("Improvement", infos.improvement)
PERCENTAGE = PercentageType("Percentage")
PROJECT = InfoType("Project", infos.project)
RELIGION = InfoType("Religion", infos.religion)
RELIGION_ADJECTIVE = ReligionAdjectiveType("ReligionAdjective")
RESOURCE = ResourceType("Resource")
ROUTES = InfosType("Routes", infos.route)
SPECIALIST = SpecialistType("Specialist")
TECH = InfoType("Tech", infos.tech)
TERRAIN = InfoType("Terrain", infos.terrain)
TURNS = TurnsType("Turns")
UNIT = InfoType("Unit", infos.unit)
UNITCOMBAT = UnitCombatType("UnitCombat")


FAILURE, POSSIBLE, SUCCESS = Enum.of("State", ("Failure", "Possible", "Success"))

SELF, VASSALS, ALLIES, STATE_RELIGION, SECULAR, WORLD = Enum.of("Subject", ("Self", "Vassals", "Allies", "StateReligion", "Secular", "World"))

STATEFUL, STATELESS = Enum.of("Mode", ("Stateful", "Stateless"))
