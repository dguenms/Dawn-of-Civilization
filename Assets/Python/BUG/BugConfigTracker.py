## BugConfigTracker
##
## Tracks the active configuration items like directory search paths and locations
## of loaded files.
##
## Copyright (c) 2008 The BUG Mod.
##
## Author: EmperorFool

import types
from CvPythonExtensions import *
localText = CyTranslator()

sortedItems = []
items = {}

def add(name, value):
	if name not in items:
		sortedItems.append(name)
	items[name] = value

def remove(name):
	if name in items:
		del items[name]
		# Leave in sorted list in case it's added later.

def combine():
	"Returns a list of tuples, where each tuple contains two elements: the name and the values as a list."
	list = []
	for name in sortedItems:
		if name in items:
			values = items[name]
			if values == None:
				values = []
			elif not isinstance(values, types.ListType):
				values = [values]
			list.append((name, values))
	return list
