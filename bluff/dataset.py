from . import *
import helpers

import random
import re

class Dataset:
	"""Class to manage a simple dataset"""
	def __init__(self, data):
		self.raw_data = data


	def random(self, data_subset=None):
		choice = None
		if data_subset is not None:
			choice = random.sample(data_subset,1).pop()
		elif self._is_list():
			choice = random.sample(self.raw_data, 1).pop()
		
		return choice

	def matches(self, filter_string, pick_random=True):
		# return a choice based on a filter string

		if self._is_list():
			# filter array
			choices = filter(lambda x: re.match(filter_string, x),self.raw_data)
			# if more then one choice left, choose randomly
			if pick_random:
				return self.random(choices)
			else:
				return list(choices)

		return list()

	def contains(self, possible_values, pick_random=True, strict=False):
		if self._is_list():
			subset = helpers.subset_from_superset(possible_values, self.raw_data)
			if pick_random:
				return self.random(subset)
			else:
				return list(subset)
		return list()


	def excludes(self, possible_values, pick_random=True, strict=False):
		if self._is_list():
			# filter array
			dataset = set(self.raw_data)
			subset = helpers.subset_from_superset(possible_values, self.raw_data)
			new_dataset = dataset.difference(subset)
			if pick_random:
				return self.random(new_dataset)
			else:
				return list(new_dataset)

		return list()


	# Private functions 

	def _is_time(self):
		if self.is_dict():
			return self.raw_data["type"] == "time"
		return False

	def _is_dict(self):
		return type(self.raw_data) is dict


	def _is_list(self):
		return type(self.raw_data) is list