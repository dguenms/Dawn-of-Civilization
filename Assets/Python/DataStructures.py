def deepdict(dictionary = {}):
	return defaultdict(dictionary, {})


def appenddict(dictionary = {}):
	return defaultdict(dictionary, [])


def defaultdict(dictionary, default):
	return DefaultDict(dictionary, default)

		
class DefaultDict(dict):

	def __init__(self, dictionary, default):
		self._default = default
		self.update(dictionary)
		
	def __getitem__(self, key):
		if not key in self:
			super(DefaultDict, self).__setitem__(key, copy(self._default))
		return super(DefaultDict, self).__getitem__(key)