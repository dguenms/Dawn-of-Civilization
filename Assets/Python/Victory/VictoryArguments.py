from Core import *


class NamedArgument(object):

	def __init__(self):
		self.name_key = ""
		
	def named(self, key):
		self.name_key = key
		return self
	
	def name(self):
		return text(self.name_key)


class AreaArgumentFactory(object):

	def __getattr__(self, name):
		area_argument = AreaArgument()
		return getattr(area_argument, name)


class AreaArgument(NamedArgument):

	def __init__(self):
		NamedArgument.__init__(self)
		
		self.calls = []
	
	def __contains__(self, item):
		return item in self.create()
	
	def __len__(self):
		return len(self.create())
	
	def __eq__(self, other):
		if not isinstance(other, AreaArgument):
			return False
			
		return self.create().same(other.create())
	
	def __repr__(self):
		return "AreaArgument%s" % "".join(".%s" % signature_name(func_name, *args, **kwargs) for func_name, args, kwargs in self.calls)
	
	def call(self, func_name, args, kwargs):
		self.calls.append((func_name, args, kwargs))
		return self
	
	def create(self):
		instance = PlotFactory()
		
		for func_name, args, kwargs in self.calls:
			instance = getattr(instance, func_name)(*args, **kwargs)
		
		if isinstance(instance, Plots):
			instance.named(self.name())
		
		return instance
	
	def of(self, *args, **kwargs):
		return self.call("of", args, kwargs)
	
	def all(self, *args, **kwargs):
		return self.call("all", args, kwargs)
	
	def rectangle(self, *args, **kwargs):
		return self.call("rectangle", args, kwargs)
	
	def regions(self, *args, **kwargs):
		return self.call("regions", args, kwargs)

	def region(self, *args, **kwargs):
		return self.call("region", args, kwargs)
	
	def capital(self, *args, **kwargs):
		return self.call("capital", args, kwargs)
	
	def where(self, *args, **kwargs):
		return self.call("where", args, kwargs)
	
	def land(self, *args, **kwargs):
		return self.call("land", args, kwargs)
	
	def owner(self, *args, **kwargs):
		return self.call("owner", args, kwargs)
	
	def without(self, *args, **kwargs):
		return self.call("without", args, kwargs)
	
	def none(self, *args, **kwargs):
		return self.create().none(*args, **kwargs)
	
	def cities(self):
		return self.create().cities()
	
	def count(self):
		return self.create().count()
		
	def closest_distance(self, *args, **kwargs):
		return self.create().closest_distance(*args, **kwargs)
		
		
class CityArgument(NamedArgument):

	def __eq__(self, other):
		if isinstance(other, CyCity):
			return at(self.get(other.getOwner()), other)
		
		return isinstance(other, type(self))

	def get(self, iPlayer):
		raise NotImplementedError()
	
	def area(self):
		raise NotImplementedError()


class LocationCityArgument(CityArgument):

	def __init__(self, *tile):
		CityArgument.__init__(self)
	
		self.tile = duplefy(*tile)
	
	def __repr__(self):
		return "LocationCityArgument%s" % (self.tile,)
	
	def __eq__(self, other):
		if not isinstance(other, LocationCityArgument):
			return CityArgument.__eq__(self, other)
		
		return self.tile == other.tile
	
	def get(self, iPlayer):
		return city(self.tile)
	
	def area(self):
		return plots.of([self.tile])


class CapitalCityArgument(CityArgument):

	def __repr__(self):
		return "CapitalCityArgument()"
	
	def get(self, iPlayer):
		return capital(iPlayer)
	
	def area(self):
		return None


class CivsArgument(NamedArgument):

	@classmethod
	def group(cls, iGroup):
		return cls(*dCivGroups[iGroup])

	def __init__(self, *identifiers):
		NamedArgument.__init__(self)
		
		self.players = players.of(*identifiers)
		
	def __repr__(self):
		return "CivsArgument(%s)" % ", ".join(infos.civ(iCiv).getShortDescription(0) for iCiv in self)
		
	def __contains__(self, identifier):
		return identifier in self.players
	
	def __eq__(self, other):
		if not isinstance(other, CivsArgument):
			return False
		
		return self.players.same(other.players)
	
	def __iter__(self):
		return iter(self.players.asCivs())
	
	def without(self, identifier):
		return CivsArgument(self.players.without(identifier))
	
	def where(self, condition):
		return CivsArgument(self.players.where(condition))
		
	def name(self):
		if not self.name_key:
			return format_separators(self, ",", text("TXT_KEY_AND"), lambda iCiv: infos.civ(iCiv).getShortDescription(0))
		
		return NamedArgument.name(self)