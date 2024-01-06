from Core import *
from unittest import *

from Slots import findSlot, addPlayer

from Pickling import pickle


bSetupComplete = False


def setup():
	global bSetupComplete
	if bSetupComplete:
		return
		
	for iSlot, iCiv in enumerate([iAssyria, iChina, iHittites, iGreece, iIndia, iPhoenicia]):
		addPlayer(6 + iSlot, iCiv, bAlive=True)
		data.dSlots[iCiv] = 6 + iSlot
	
	for i in [3, 4, 5]:
		unit = makeUnit(i, iMilitia, (i, 0))
		player(i).verifyAlive()
		unit.kill(False, -1)
	
	bSetupComplete = True


class PickleTestCase(TestCase):

	def assertPickleable(self, object):
		print "assert pickle %s" % object.__class__.__name__
		self.tryPickle(object)
			
	def tryPickle(self, object):
		try:
			pickle.dumps(object)
		except:
			if hasattr(object, '__dict__'):
				for key, value in object.__dict__.iteritems():
					print "try pickle %s" % key
					self.tryPickle(value)
			raise