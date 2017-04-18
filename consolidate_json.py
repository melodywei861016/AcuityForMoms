import json

final_database = 'MainDatabaseFile.json'

def load_data(file_name):
	with open(file_name) as data_file:    
		data = json.load(data_file)
	return data 

def dump_data(file_name, data):
	with open(file_name, 'w') as outfile:
		json.dump(data, outfile)

def consolidate_data(data):
	""" Note: data is a list of lists of courses. 
		Makes it easily scalable i.e. just append new list of 
		courses to the list argument (data)
	"""
	result = {}

	for datum in data:
		for key, value in datum.items():
			result[key] = value

	print len(result.items())
	dump_data(final_database, result)

udacity_data = load_data('UdacityDatabaseFile.json')
udemy_data = load_data('UdemyDatabaseFile.json')
edx_data = load_data('EdXDatabaseFile.json')

#consolidate_data([udacity_data, udemy_data, edx_data]) 

