from Core import *


class Progress(object):
		
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


PROGRESS = Progress()