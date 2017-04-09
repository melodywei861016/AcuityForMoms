import requests, json, pickle
from requests.auth import HTTPBasicAuth
from datetime import datetime

import requests # pip install requests

url = 'https://api.edx.org/oauth2/v1/access_token'
r = requests.post(url, dict(
	grant_type='client_credentials',
	client_id='14TIRydxjYn2TTzKBjo1PHddKtClV3DEOeWnZCBL',
	client_secret='XiqlqBFgCwpj6WajRndn3A2hX77nzq6pd1ujkmtwuM6ixzQcsaNoXdk7cDyNteKrVpoauXs9WBvsEHkMgomfknW1YPuJtExRYOKdOtvG3LY6fjwaHxi5v0AuFX5AQusW',
	token_type='jwt'))

access_token = json.loads(r.text)['access_token']

headers = {
    'Authorization': 'JWT ' + access_token,
}

def make_response(url):
	response = requests.get(url, headers=headers)
	json_response = json.loads(response.text)
	return json_response

full_catalog_info =  make_response('https://api.edx.org/catalog/v1/catalogs/')['results'][0]

json_response = make_response('https://api.edx.org/catalog/v1/catalogs/' + str(full_catalog_info['id']) + '/courses')

#print(json_response['results'])

#print(json_response['results'][0]['course_runs'])


database = {}
pulledDictionary = {}

#Adding EdX courses to the database
def create_database():
	for course in json_response['results']:
	    dictionary_elem = course['key']
	    database[dictionary_elem] = {} #the course's key is the key to the dictionary. Its corresponding value is a dictionary of the course's components (time, cost, etc.)

	    database[dictionary_elem]['title'] = course['title']
	    database[dictionary_elem]['homepage'] = course['marketing_url']
	    database[dictionary_elem]['short description'] = course['short_description']
	    database[dictionary_elem]['level'] = course['level_type'] 
	    database[dictionary_elem]['prerequisites'] = course['prerequisites']
	    database[dictionary_elem]['expected learning'] = course['expected_learning_items']
	    database[dictionary_elem]['image'] = course['image']['src']
	    database[dictionary_elem]['owner name'] = course['owners'][0]['name']	    
	    
	    if course['course_runs'][0]['start'] != None and course['course_runs'][0]['end'] != None:
	    	#subtract the date to get weeks
	    	start_date = datetime.strptime(course['course_runs'][0]['start'][:19], "%Y-%m-%dT%H:%M:%S")
	    	end_date = datetime.strptime(course['course_runs'][0]['end'][:19], "%Y-%m-%dT%H:%M:%S")
	    	duration = (end_date - start_date).days//7 #duration length in weeks
	    else:
	    	duration = 'undetermined'
	    database[dictionary_elem]['time to complete'] = duration
	    
	    database[dictionary_elem]['price'] = course['course_runs'][0]['seats'][0]['price'] + ' ' + course['course_runs'][0]['seats'][0]['currency']
	    #database[dictionary_elem]['availablility_status'] = course['full_course_available']
	    
	with open('EdXDatabaseFile.json', 'w') as myFile:
		json.dump(database, myFile)

def read_database_text_file():
	global pulledDictionary
	with open('EdXDatabaseFile.txt', 'rb') as myFile:
		pulledDictionary = pickle.load(myFile)

def read_database_json_file():
	return json.loads(open('EdXDatabaseFile.json').read())








