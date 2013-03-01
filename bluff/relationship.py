from . import *
import itertools

class Relationship:
	"""Class to manage a simple relationship as defined by a JSON format"""
	def __init__(self, relationship):
		self.relationship = relationship
		
		self.seed_keys = set(relationship["keys"]) # always required, should throw an exception if not found

		self.seed_rules = {}

		self.seeds = {}


	def add_seed(self, new_seed):
		self.seeds[new_seed.name] = new_seed

		seed_name = new_seed.name
		if seed_name in self.relationship:
			self.seed_rules[seed_name] = self._parse_rules(self.relationship[seed_name])

	def get_target_seed(self, origin_seed_name):
		seed_name = self.seed_keys.difference(set([origin_seed_name])).pop()
		return self.seeds[seed_name]

	# Private methods

	def _parse_rules(self,rules):
		if len(rules.keys()) == 1:
			if "matches" in rules:
				return [MatchRule(rules)]

			if "contains" in rules:
				return [ContainsRule(rules)]

			if "missing" in rules:
				return [MissingRule(rules)]
		else:
			l = list()
			copied_rules = dict(rules)
			first_key = copied_rules.keys().pop()
			l.append(self._parse_rules({first_key :  copied_rules.pop(first_key)}))
			l.append(self._parse_rules(copied_rules))
			return list(itertools.chain.from_iterable(l))


class RelationshipRule:
	@staticmethod
	def parse(rules):
		if "matches" in rules:
			return MatchRule(rules)

		if "contains" in rules:
			return ContainsRule(rules)

		if "missing" in rules:
			return MissingRule(rules)


class MatchRule(RelationshipRule):
 	def __init__(self, rules):
		self.matches = rules["matches"] # a regex pattern to use on the parent seed
		self.searches = self.matches.keys() 
	
	# supports contains or excludes
	def contains(self, key):
		skey = "sibling-contains"
		if skey not in self.matches[key]:
			return None
		return self.matches[key][skey]

	def excludes(self, key):
		skey = "sibling-excludes"
		if skey not in self.matches[key]:
			return None
		return self.matches[key][skey]


class ContainsRule(RelationshipRule):
 	def __init__(self, rules):
		self.contains = rules["contains"] #could be an array
		self.values = self.contains["values"]
		self.matches = None

		skey = "sibling-matches"
		if skey in self.contains:
			self.matches = self.contains[skey]


class MissingRule(RelationshipRule):
	def __init__(self, rules):
		self.missing = rules["missing"] # a regex pattern to use on the parent seed
		self.values = self.missing["values"]
		self.matches = None

		skey = "sibling-matches"
		if skey in self.missing:
			self.matches = self.missing[skey]


