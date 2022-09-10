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


def format_articles(string):
	return string.replace("The", "the")


def remove_articles(string):
	return string.lstrip("the").lstrip()


def number_word(number):
	return text_if_exists("TXT_KEY_VICTORY_NUMBER_%s" % number, otherwise=number)


def ordinal_word(number):
	return text_if_exists("TXT_KEY_VICTORY_ORDINAL_%s" % number, otherwise="%d%s" % (number, text("TXT_KEY_VICTORY_ORDINAL_DEFAULT_SUFFIX")))


def qualify(string, qualifier, condition):
	if condition:
		return text(qualifier, string)
	return string


def qualify_adjective(string, type, qualifier):
	if qualifier is not None:
		return "%s %s" % (type.format(qualifier), string)
	return string


def indicator(value):
	symbol = value and FontSymbols.SUCCESS_CHAR or FontSymbols.FAILURE_CHAR
	return u"%c" % game.getSymbolID(symbol)


def capitalize(string):
	if not string:
		return string
	
	return string[0].upper() + string[1:]


def format_date_turn(iYear, with_turn=False):
	if with_turn:
		return "%s (%s)" % (format_date(iYear), text("TXT_KEY_VICTORY_TURN", year(iYear) - scenarioStartTurn()))
	
	return format_date(iYear)

