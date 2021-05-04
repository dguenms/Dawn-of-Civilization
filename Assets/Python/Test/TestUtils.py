from unittest import *

import cPickle as pickle


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