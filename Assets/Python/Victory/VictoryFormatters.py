from Core import *

from VictoryTypes import *

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


def qualify(string, qualifier, condition):
	if condition:
		return text(qualifier, string)
	return string


def qualify_adjective(string, type, qualifier):
	if qualifier is not None:
		return "%s %s" % (type.format(qualifier), string)
	return string
	

def in_area(string, area):
	if area is not None:
		return text("TXT_KEY_VICTORY_IN_AREA", string, AREA.format(area))
	return string


def with_religion(string, iReligion):
	if iReligion is not None:
		return text("TXT_KEY_VICTORY_WITH_RELIGION", string, RELIGION_ADJECTIVE.format(iReligion))
	return string


def indicator(value):
	symbol = value and FontSymbols.SUCCESS_CHAR or FontSymbols.FAILURE_CHAR
	return u"%c" % game.getSymbolID(symbol)


def capitalize(string):
	if not string:
		return string
	
	return string[0].upper() + string[1:]

