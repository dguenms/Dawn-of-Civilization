from Core import *

from itertools import chain

import os
import csv
import cStringIO

MAPS_PATH = "Assets/Maps"


def getPath(file_name):
	return "%s\Mods\\RFC Dawn of Civilization\\Assets\\Maps\\%s" % (os.getcwd(), file_name)


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8").encode("utf-8")
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class FileMap(object):

	@staticmethod
	def is_valid_value(value):
		if value is None:
			return False
		
		if value == "":
			return False
		
		return True
	
	@staticmethod
	def parse(value):
		try:
			return int(value)
		except ValueError:
			return value.decode("utf8")

	@classmethod
	def read(cls, file_path):
		try:
			file = open(getPath(file_path))
		except IOError:
			return
		
		try:
			for y, line in enumerate(reversed(list(csv.reader(file)))):
				for x, value in enumerate(line):
					if cls.is_valid_value(value):
						yield (x, y), cls.parse(value)
		except:
			file.close()
			raise
		
		file.close()
	
	@staticmethod
	def write(rows, file_path):
		file = open(getPath(file_path), "wb")
		writer = UnicodeWriter(file)
		
		try:
			for row in reversed(rows):
				row = [cell and cell or u"" for cell in row]
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
		if self.map is None:
			self.load()
		
		self.write(self.map, "Export/%s" % self.path)


class FileDict(object):

	@staticmethod
	def read(file_path):
		try:
			file = open(getPath(file_path))
		except IOError:
			return
		
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
