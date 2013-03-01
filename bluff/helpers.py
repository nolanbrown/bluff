import re

def subset_from_superset(filter_values, dataset, strict=False):
	subset = set()
	for device in dataset:
		for dsub in filter_values:
			if strict is False:
				if re.match(dsub, device):
					#print dsub + " = " + device
					subset.add(device)
			else:
				if dsub is device:
					subset.add(device)
	return subset
