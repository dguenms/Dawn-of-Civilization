from Core import *
from Types import *
	

def in_area(string, area):
	if area is not None:
		return text("TXT_KEY_VICTORY_IN_AREA", string, AREA.format(area))
	return string


def outside_area(string, area):
	if area is not None:
		return text("TXT_KEY_VICTORY_OUTSIDE_AREA", string, AREA.format(area))
	return string


def religion_adjective(string, iReligion):
	if iReligion is not None:
		return text("TXT_KEY_VICTORY_RELIGION_ADJECTIVE", string, RELIGION_ADJECTIVE.format(iReligion))
	return string
	

def with_religion_in_cities(string, iReligion):
	if iReligion is not None:
		return text("TXT_KEY_VICTORY_WITH_RELIGION_IN_CITIES", string, RELIGION.format(iReligion))
	return string


class Description(object):
	
	def __init__(self, key, *arguments):
		self.key = key
		self.arguments = arguments
	
	def __repr__(self):
		return "Description(key=%s, arguments=%s)" % (self.key, self.arguments)
	
	def __eq__(self, other):
		if not isinstance(other, Description):
			return False
		
		return self.key == other.key and self.arguments == other.arguments
	
	def format(self):
		return text(self.key, *self.arguments)
	
	def matches(self, desc):
		return False
	
	def unwrap(self):
		return [self]


class WrappedDescription(Description):
	
	def __init__(self, key, description, *arguments):
		Description.__init__(self, key, *arguments)
		
		self.description = description
	
	def __repr__(self):
		return "WrappedDescription(key=%s, description=%s, arguments=%s)" % (self.key, self.description, self.arguments)
	
	def __eq__(self, other):
		if not isinstance(other, WrappedDescription):
			return False
		
		return Description.__eq__(self, other) and self.description == other.description
	
	def format(self):
		return text(self.key, self.description.format(), *self.arguments)
	
	def matches(self, desc):
		if not isinstance(desc, WrappedDescription):
			return False
		
		return self.key == desc.key and self.arguments == desc.arguments
	

class CombinedDescription(Description):
	
	def __init__(self, descriptions):
		self.descriptions = descriptions
	
	def __repr__(self):
		return "CombinedDescription(%s)" % (self.descriptions,)
	
	def __eq__(self, other):
		if not isinstance(other, CombinedDescription):
			return False
		
		return self.descriptions == other.descriptions
	
	def format(self):
		return format_separators(self.descriptions, ", ", text("TXT_KEY_AND"), format=lambda desc: desc.format())
	
	def matches(self, desc):
		return False
	
	def unwrap(self):
		return self.descriptions
		

def generate_description(entries, key, arguments, suffixes, required):
	description = combine_entries(entries)
	
	if is_identical_threshold_requirement(entries):
		first = entries[0]
		description = WrappedDescription(entries[0].DESC_KEY, combine_descriptions([Description(entry.format_parameters(bPlural=True)[0]) for entry in entries]), first.format_parameters(bPlural=True)[-1])
	
	if required:
		description = WrappedDescription("TXT_KEY_VICTORY_REQUIRED_OUT_OF", description, COUNT.format(required))
	
	if key:
		description = WrappedDescription(key, description, *arguments)
	
	for suffix in suffixes:
		description = WrappedDescription("TXT_KEY_VICTORY_SUFFIX", description, suffix)
	
	return description


def is_identical_threshold_requirement(entries):
	if len(entries) < 2:
		return False
	
	first = entries[0]
	
	if not hasattr(first.__class__, "TYPES"):
		return False
	
	if len(first.TYPES) != 2:
		return False
	
	if first.TYPES[-1] != COUNT:
		return False
	
	if first.parameters[-1] == 1:
		return False
	
	if first.TYPES[0] == ERA:
		return False
	
	return all(entry.parameters[-1] == first.parameters[-1] for entry in entries)


def combine_entries(entries):
	return combine_descriptions([entry.get_description() for entry in entries])


def combine_descriptions(descs):
	if len(descs) == 1:
		return descs[0]
	
	combined = []
	groups = []
	previous_desc = None
	
	for desc in descs:
		if previous_desc and desc.matches(previous_desc):
			groups[-1].append(desc)
		else:
			groups.append([desc])
		
		previous_desc = desc
	
	for group in groups:
		if len(group) == 1:
			combined.append(group[0])
		else:
			combined.append(WrappedDescription(group[0].key, combine_descriptions(sum((desc.description.unwrap() for desc in group), [])), *group[0].arguments))
	
	if len(combined) == 1:
		return combined[0]
	
	return CombinedDescription(combined)
	


class ProgressFormatter(object):
		
	def format(self, requirements, evaluator):
		list_progress = self.format_list(requirements, evaluator)
		item_progress = self.format_items(requirements, evaluator)
		
		return list(list_progress) + list(item_progress)
		
	def format_list(self, requirements, evaluator):
		for requirement in requirements:
			progress = requirement.progress(evaluator)
			if isinstance(progress, list):
				for row in progress:
					yield row
	
	def format_items(self, requirements, evaluator):
		item_progress = self.get_item_progress(requirements, evaluator)
		row_size = self.get_row_size(item_progress)
		
		for index in range(0, len(item_progress), row_size):
			yield " ".join(progress for progress in item_progress[index:index+row_size])
		
	def get_item_progress(self, requirements, evaluator):
		item_progress = [requirement.progress(evaluator) for requirement in requirements]
		return [progress for progress in item_progress if not isinstance(progress, list)]
	
	def get_row_size(self, items):
		if len(items) % 4 == 0:
			return 4
		elif len(items) % 3 == 0:
			return 3
		elif len(items) % 4 > len(items) % 3:
			return 4
		else:
			return 3



PROGRESS = ProgressFormatter()

