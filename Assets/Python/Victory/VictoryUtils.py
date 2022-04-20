from Core import *

import re


IRREGULAR_PLURALS = {
	"Ship of the Line": "Ships of the Line",
	"Great Statesman": "Great Statesmen",
	"cathedral of your state religion": "cathedrals of your state religion",
}


def plural(word):
	if not word:
		return word

	if word in IRREGULAR_PLURALS:
		return IRREGULAR_PLURALS[word]

	if word.endswith('s'):
		return word
	
	if word.endswith('y'):
		return re.sub('y$', 'ies', word)
	
	if word.endswith('ch') or word.endswith('sh'):
		return word + 'es'
	
	if word.endswith('man'):
		return re.sub('man$', 'men', word)
	
	return word + 's'


def number_word(number):
	return text_if_exists("TXT_KEY_VICTORY_NUMBER_%s" % number, otherwise=number)


def ordinal_word(number):
	return text_if_exists("TXT_KEY_VICTORY_ORDINAL_%s" % number, otherwise="%d%s" % (number, text("TXT_KEY_UHV_ORDINAL_DEFAULT_SUFFIX")))


class AreaDefinitionFactory(object):

	def __getattr__(self, name):
		area_definition = AreaDefinition()
		return getattr(area_definition, name)


class AreaDefinition(object):

	def __init__(self):
		self.name_key = ""
		self.calls = []
	
	def __contains__(self, item):
		return item in self.create()
	
	def __len__(self):
		return len(self.create())
	
	def __eq__(self, other):
		if not isinstance(other, AreaDefinition):
			return False
			
		return self.create().same(other.create())
	
	def __repr__(self):
		return "AreaDefinition%s" % "".join(".%s" % signature_name(func_name, *args, **kwargs) for func_name, args, kwargs in self.calls)
	
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
	
	def named(self, key):
		self.name_key = key
		return self
	
	def name(self):
		return text(self.name_key)
	
	def cities(self):
		return self.create().cities()


def indicator(value):
	symbol = value and FontSymbols.SUCCESS_CHAR or FontSymbols.FAILURE_CHAR
	return u"%c" % game.getSymbolID(symbol)


plots = AreaDefinitionFactory()

