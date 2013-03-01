from . import *
import helpers
class Seed:
	"""Class to manage a simple dataset"""
	def __init__(self, key, model):
		self.name = key
		self.relationships = {}

		self.data = Dataset(model)

	def add_relationship(self, rel_obj):
		# accept a relationship object and store a reference by target seed name
		seed_keys = list(rel_obj.seed_keys)
		if len(seed_keys) is not 2:
			raise "Invalid Relationship"
		seed_keys.remove(self.name) # remove the current seed name, remaining name is target
		target_seed_name = seed_keys.pop()
		self.relationships[target_seed_name] = rel_obj


	def generate(self, data):
		relevent_relationships = []
		if data is not None: # check data for already generated relationship data
			for key in self.relationships.keys():
				if key in data: # a relationship has already had data generated
					relevent_relationships.append({"relationship" : self.relationships[key], "value" : data[key], "key" :  key})

		if len(relevent_relationships) > 0: ## there are relationships that we have to use to generate our values
			return self._generate_value_with_relationships(relevent_relationships)
		else:
			return self.data.random() ## extract a random value

	# Private Functions

	def _generate_value_with_relationships(self, relevent_relationships):
		sets = set()
		for r in relevent_relationships:
			# returns a value based on the relationship
			# DOES not take into account both relationships
			sets.add(self._value_for_seed_with_given_value(r["relationship"],r["value"]))

		if len(sets) == 0:
			return None
		else:
			random_value = self.data.random(sets)
			return random_value



	def _value_for_seed_with_given_value(self, relationship, value):
		# get target seed (not the one passed in)
		target_seed = relationship.get_target_seed(self.name) # value is the already generated value for this seed

		# check seed name for seed rules
		rules = relationship.seed_rules[target_seed.name] # 

		possible_values = set() # array of sets
		for rule in rules:
			rule_type = rule.__class__.__name__ 
			if rule_type is "MatchRule":
				data_set = self._match(rule, value, self.data)
				if data_set:
					possible_values.update(data_set)

			elif rule_type is "ContainsRule":
				data_set = self._contains(rule, value, self.data)
				if data_set:
					possible_values.update(data_set)

			elif rule_type is "MissingRule":
				data_set = self._missing(rule, value, self.data)
				if data_set:
					possible_values.update(data_set)

		#print possible_values
		if len(possible_values) == 0: # how can we tell if no available values or that any value is valid
			return None # self.data.random()
		else:
			return self.data.random(possible_values)
		## subtract all sets 


	def _contains(self, rule, value, dataset):
		# if model contains the values, then the current seed should be generated using sibling-matches 
		subset = helpers.subset_from_superset(rule.values, [value])
		if len(subset) > 0: # subset will never be larger then 1
			m = rule.matches
			if m:
				return set([dataset.matches(m)])
		return None

	def _missing(self, rule, value, dataset):
		# if model contains the values, then the current seed should be generated using sibling-matches 
		# print "Missing Checking Value: " + value
		# print "Missing Checking Against: " 
		# print rule.values

		subset = helpers.subset_from_superset(rule.values, [value])
		# value matches check values
		if len(subset) is 0: # subset will never be larger then 1
			# then generate based on the maches algo
			m = rule.matches
			if m:
				return set([dataset.matches(m)])
		return None


	def _match(self, rule, value, dataset):
		for search_string in rule.searches:
			# value matches search string
			if re.match(search_string, value): 	# if match is found,
				c = rule.contains(search_string) # check for contains 
				if c:
					return set(dataset.contains(c, False)) # call dataset
				e = rule.excludes(search_string) # check for excludes
				if e:
					return set(dataset.excludes(e, False)) # call dataset




