import requests, json
from requests.auth import HTTPBasicAuth

database = {}

def make_response(url):
	response = requests.get(url, auth=requests.auth.HTTPBasicAuth('iPDNTWkvRJuOJSXsPYAD0iw2UXWtQgoiYquEITqq','blPILgbSF2AJjWDSvfTA4xcFduXk1l4DQfuEdl6iYWe6j4GGphW6XGtmdn67Lo5fSpUjMP9zZLoYWpBpk3dyQFXQLTJUYHDdzZsl3RfGTQZcEzeaKovfytJJIBXAmh8x'))
	json_response = json.loads(response.text)
	return json_response

json_response = make_response('https://www.udemy.com/api-2.0/courses/?page=1')

#Adding Udemy courses to the database
while 'detail' not in json_response.keys():
	for course in json_response['results']:
		dictionary_elem = course['id']
		database[dictionary_elem] = {}

		database[dictionary_elem]['title'] = course['title']
		database[dictionary_elem]['homepage'] = 'https://www.udemy.com' + course['url']
		short_description_response = make_response('https://www.udemy.com/api-2.0/courses/{}?fields[course]=headline'.format(course['id']))
		database[dictionary_elem]['short description'] = short_description_response['headline']
		level_response = make_response('https://www.udemy.com/api-2.0/courses/{}?fields[course]=instructional_level'.format(course['id']))
		database[dictionary_elem]['level'] = level_response['instructional_level']
		database[dictionary_elem]['image'] = course['image_480x270']
		database[dictionary_elem]['price'] = course['price']
	    
	    #database[dictionary_elem]['prerequisites']
	    #database[dictionary_elem]['expected learning']
	    #database[dictionary_elem]['owner name']
	    #database[dictionary_elem]['time to complete'] = str(course['expected_duration']) + " " + course['expected_duration_unit']
	    #database[dictionary_elem]['availablility_status'] = course['full_course_available']
	    
	    #Getting the category of the course
		    #course_category_response = make_response('https://www.udemy.com/api-2.0/courses/{}?fields[course]=primary_category'.format(course['id']))
			#course_category_id = course_category_response['primary_category']['id']
			#course_category_name = course_category_response['primary_category']['title']
	    
	url = json_response['next']


print(database)





