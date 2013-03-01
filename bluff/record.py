import random
from . import *


class Record:
	"""
	Given a set of randomly ordered seeds, Record will extract values from seeds based on relationships defined in the seeds
	"""
	def __init__(self, seeds):
		# copy a new instance of the seeds to prevent modification
		self.seeds = seeds.copy()
		
		self.seed_keys = self.seeds.keys()

		# randomly order seeds so no model key takes priority over other keys
		random.shuffle(self.seed_keys)
		self.data = {}

	def build(self):
		# print self.seed_keys
		for i in range(len(self.seed_keys)):
			skey = self.seed_keys[i]
			seed = self.seeds[skey]
			self.data[skey] = seed.generate(self.data)

		#print self.data
		return self.data
