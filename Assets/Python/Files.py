from Core import *

import os
import csv

MAPS_PATH = "Assets/Maps"


def getPath(file_name):
	return "%s\Mods\\RFC Dawn of Civilization\\Assets\\Maps\\%s" % (os.getcwd(), file_name)


class FileMap(object):

	@staticmethod
	def is_valid_value(value):
		if value is None:
			return False
		
		if value == "":
			return False
		
		return True
	
	@staticmethod
	def cast_value(value):
		try:
			return int(value)
		except ValueError:
			return value

	@classmethod
	def read(cls, file_path):
		file = open(getPath(file_path))
		
		try:
			for y, line in enumerate(reversed(list(csv.reader(file)))):
				for x, value in enumerate(line):
					if cls.is_valid_value(value):
						yield (x, y), cls.cast_value(value)
		except:
			file.close()
			raise
		
		file.close()
	
	@staticmethod
	def write(rows, file_path):
		file = open(getPath(file_path), "wb")
		writer = csv.writer(file)
		
		try:
			for row in reversed(rows):
				writer.writerow(row)
		finally:
			file.close()

	def __init__(self, map_path):
		self.path = map_path
		self.map = None
	
	def __getitem__(self, tile):
		if self.map is None:
			self.load()
		
		x, y = location(tile)
		return self.map[y][x]
	
	def __iter__(self):
		for x in range(iWorldX):
			for y in range(iWorldY):
				value = self[x, y]
				if self.is_valid_value(value):
					yield (x, y), value
	
	def create(self, values):
		map = [[None for x in range(iWorldX)] for y in range(iWorldY)]
		
		for (x, y), value in values:
			map[y][x] = value
		
		self.map = tuple(tuple(row) for row in map)
	
	def load(self):
		self.create(self.read(self.path))
	
	def update(self, other):
		self.create(chain(iter(self), iter(other)))
	
	def export(self):
		if self.map is not None:
			self.write(self.map, "Export/%s" % self.path)


class FileDict(object):

	@staticmethod
	def read(file_path):
		file = open(getPath(file_path))
		
		try:
			for line in csv.reader(file):
				if len(line) < 2:
					continue
				
				yield line[:2]
		except:
			file.close()
			raise
		
		file.close()

	def __init__(self, path):
		self.path = path
		self.dict = None
	
	def __getitem__(self, key):
		if self.dict is None:
			self.load()
	
		return self.dict[key]
	
	def __setitem__(self, key, value):
		if self.dict is None:
			self.load()
		
		self.dict[key] = value
	
	def __contains__(self, key):
		if self.dict is None:
			self.load()
		
		return key in self.dict
	
	def load(self):
		self.dict = {}
	
		for key, value in self.read(self.path):
			self[key] = value
	
	def values(self):
		if self.dict is None:
			self.load()
		
		return self.dict.values()
