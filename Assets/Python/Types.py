from CvPythonExtensions import *


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