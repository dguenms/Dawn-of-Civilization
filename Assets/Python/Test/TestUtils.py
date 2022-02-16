from Core import *
from unittest import *

from Scenario import addPlayer

import cPickle as pickle


bSetupComplete = False


def setup():
	global bSetupComplete
	if bSetupComplete:
		return

	addPlayer(iChina)
	addPlayer(iIndia)
	
	data.dSlots[iChina] = 7
	data.dSlots[iIndia] = 8
	
	for i in [4, 5, 6]:
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