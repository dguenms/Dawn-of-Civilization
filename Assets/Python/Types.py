from CvPythonExtensions import *


def null(cls, name, *args, **kwargs):
	def __init__(self, *args, **kwargs):
		cls.__init__(self, *args, **kwargs)
	
	def __call__(self, *args, **kwargs):
		return 0
	
	def __getattribute__(self, name):
		return self
		
	def __setattr__(self, name, value):
		return self
		
	def __delattr__(self, name):
		return self
	
	def __nonzero__(self):
		return False
		
	funcs = (__init__, __call__, __getattribute__, __setattr__, __delattr__, __nonzero__)
	return type(name, (cls,), dict((func.__name__, func) for func in funcs))


NullCity = null(CyCity, "NullCity")


class NullPlayer(CyPlayer):

	def __init__(self, *args, **kwargs):
		super(NullPlayer, self).__init__(*args, **kwargs)
	
	def __call__(self, *args, **kwargs):
		return self
	
	def __getattribute__(self, name):
		return self
		
	def __setattr__(self, name, value):
		return self
		
	def __delattr__(self, name):
		return self
	
	def __nonzero__(self):
		return False


class NullTeam(CyTeam):

	def __init__(self, *args, **kwargs):
		super(NullTeam, self).__init__(*args, **kwargs)
	
	def __call__(self, *args, **kwargs):
		return self
	
	def __getattribute__(self, name):
		return self
		
	def __setattr__(self, name, value):
		return self
		
	def __delattr__(self, name):
		return self
	
	def __nonzero__(self):
		return False


class Civ(int):

	def __new__(cls, value, *args, **kwargs):
		return super(cls, cls).__new__(cls, value)


NoCiv = Civ(-1)