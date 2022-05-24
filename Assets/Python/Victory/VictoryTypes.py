from Core import *
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


class Aggregate(object):

	def __init__(self, *items):
		self.items = list(variadic(*items))
	
	def __repr__(self):
		return "%s(%s)" % (type(self).__name__, ", ".join(str(item) for item in self.items))
	
	def __contains__(self, item):
		return item in self.items
	
	def __eq__(self, other):
		if isinstance(other, Aggregate):
			return self.items == other.items
		
		return other in self
	
	def validate(self, validate_func):
		return all(validate_func(item) for item in self.items)
	
	def format(self, format_func, **options):
		return format_separators(self.items, ",", text("TXT_KEY_AND"), lambda item: format_func(item, **options))
	
	def evaluate(self, evaluate_func):
		return self.aggregate([evaluate_func(item) for item in self.items])
	
	def aggregate(self, items):
		raise NotImplementedError()


class SumAggregate(Aggregate):

	def aggregate(self, items):
		return sum(items)


class AverageAggregate(Aggregate):

	def aggregate(self, items):
		if len(items) == 0:
			return 0.0
		return 1.0 * sum(items) / len(items)


class CountAggregate(Aggregate):

	def aggregate(self, items):
		return count(items)


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
		return self.format_func(argument, **options)
	
	def format_repr(self, argument):
		if isinstance(argument, Aggregate):
			return argument.format(self.format_repr_func)
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
		return isinstance(argument, int)
	
	def format_func(self, argument, bPlural=False, **options):
		text = self.info(argument).getText()
		if bPlural:
			return plural(text)
		return text
		
		
class CountType(Type):
	
	def validate_func(self, argument):
		return isinstance(argument, int)
	
	def format_func(self, argument, **options):
		return number_word(argument)
	
	def format_repr_func(self, argument):
		return str(argument)


class AreaType(Type):

	def validate_func(self, argument):
		return isinstance(argument, AreaDefinition)
	
	def format_func(self, argument, **options):
		return argument.name()


class PercentageType(Type):

	def validate_func(self, argument):
		return isinstance(argument, int)
	
	def format_func(self, argument, **options):
		return "%d%%" % argument


class CityType(Type):

	def validate_func(self, argument):
		return isinstance(argument, CityDefinition)
	
	def format_func(self, argument):
		return argument.name()


AMOUNT = SimpleType("Amount", int)
AREA = AreaType("Area")
BUILDING = InfoType("Building", infos.building)
CITY = CityType("City")
COUNT = CountType("Count")
PERCENTAGE = PercentageType("Percentage")
TECH = InfoType("Tech", infos.tech)


FAILURE, POSSIBLE, SUCCESS = Enum.of("State", ("Failure", "Possible", "Success"))

SELF, VASSALS, ALLIES, RELIGION, SECULAR, WORLD = Enum.of("Subject", ("Self", "Vassals", "Allies", "Religion", "Secular", "World"))

STATEFUL, STATELESS = Enum.of("Mode", ("Stateful", "Stateless"))