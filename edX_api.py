import requests, json, pickle
from requests.auth import HTTPBasicAuth

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

index = len(json_response['results']) - 1

#Adding EdX courses to the database
def create_database():
	global index
	while index >= 0:

	    dictionary_elem = json_response['results'][index]['key']
	    database[dictionary_elem] = {} #the json_response['results'][index]'s key is the key to the dictionary. Its corresponding value is a dictionary of the json_response['results'][index]'s components (time, cost, etc.)

	    database[dictionary_elem]['title'] = json_response['results'][index]['title']
	    database[dictionary_elem]['homepage'] = json_response['results'][index]['marketing_url']
	    database[dictionary_elem]['short description'] = json_response['results'][index]['short_description']
	    database[dictionary_elem]['level'] = json_response['results'][index]['level_type'] 
	    database[dictionary_elem]['prerequisites'] = json_response['results'][index]['prerequisites']
	    database[dictionary_elem]['expected learning'] = json_response['results'][index]['expected_learning_items']
	    database[dictionary_elem]['image'] = json_response['results'][index]['image']['src']
	    database[dictionary_elem]['owner name'] = json_response['results'][index]['owners'][0]['name']

	    """
	    if course['course_runs'][0]['start'] != 'None':
	    	#subtract the date to get weeks
	    	duration = course['course_runs'][0]['end'] - course['course_runs'][0]['start']
	    	total_time = duration * course['course_runs'][0]['min_effort'] #the total number of minimum hours over all the weeks
	    else:
	    	total_time = 'up to user'
	    database[dictionary_elem]['time to complete'] = total_time
	    """

	    database[dictionary_elem]['price'] = json_response['results'][index]['course_runs'][0]['seats'][0]['price'] + ' ' + json_response['results'][index]['course_runs'][0]['seats'][0]['currency']
	    #database[dictionary_elem]['availablility_status'] = course['full_course_available']
	    with open('EdXDatabaseFile.txt', 'wb') as myFile:
	    	pickle.dump(database, myFile)

	    print(index)
	    index -= 1
	    


with open('EdXDatabaseFile.txt', 'rb') as myFile:
	pulledDictionary = pickle.load(myFile)








