import random
from . import *


class Manager:
	"""
	Manages a set of Records
	"""
	def __init__(self, seed_data):
		self.seeds = {}
		self.relationships = []
		self.records = []

		if "dataset" in seed_data:
			for model_key in seed_data["dataset"]:
				mkey = str(model_key)
				self.seeds[mkey] = Seed(mkey, seed_data["dataset"][mkey])

		## assign relationships to seeds
		if "relationships" in seed_data:
			for relationship in seed_data["relationships"]: # relationship is a dict object
				r = Relationship(relationship)
				for skey in r.seed_keys: # identify relationship seeds
					seed = self.seeds[skey]
					r.add_seed(seed) # add seed to relationship
					seed.add_relationship(r) # add relationship to seed

				self.relationships.append(r)

	def generate(self, num_instances=100):
		for i in range(num_instances):
			r = Record(self.seeds)
			generated_row = r.build()
			self.records.append(generated_row)
		return self.records
