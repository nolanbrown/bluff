#!/usr/bin/env python

import sys 
import pymongo
from pymongo import MongoClient
import json
from bluff import *




def main():
	dataset_contents = open('dataset.blf').read()
	seed_data = json.loads(dataset_contents)

	connection = MongoClient()
	db = connection['bluff']
	
	manager = Manager(seed_data)
	records = manager.generate(100)
	db.devices.insert(records)

	#print json.dumps(records)

if __name__ == "__main__":
    main()
