import requests, json, pickle, urllib, urllib.request, httplib2
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

database = {}

def make_response(url):
	response = requests.get(url, auth=requests.auth.HTTPBasicAuth('iPDNTWkvRJuOJSXsPYAD0iw2UXWtQgoiYquEITqq','blPILgbSF2AJjWDSvfTA4xcFduXk1l4DQfuEdl6iYWe6j4GGphW6XGtmdn67Lo5fSpUjMP9zZLoYWpBpk3dyQFXQLTJUYHDdzZsl3RfGTQZcEzeaKovfytJJIBXAmh8x'))
	json_response = json.loads(response.text)
	return json_response

current_url = 'https://www.udemy.com/api-2.0/courses/?page=1&page_size=100'
json_response = make_response(current_url)

#Adding Udemy courses to the database
def create_database():
	"""Instructions: How to form the database file: 
		1) execute the file in the interpreter
		2) execute create_database()
		3) when interpreter stops, execute create_database again
		4) type this into the interpreter (without exiting the program) to check how long you need to wait before executing the function create_database() again: print(make_response('https://www.udemy.com/api-2.0/courses/{}?fields[course]=headline'.format('437398')))
		4) execute the function until there are no more errors
		5) The database file should be formed
	"""
	global json_response, current_url
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
			database[dictionary_elem]['rating'] = course['avg_rating']
		    
		    #database[dictionary_elem]['availablility_status'] = course['full_course_available']
		    
		    #Getting the category of the course
		    #course_category_response = make_response('https://www.udemy.com/api-2.0/courses/{}?fields[course]=primary_category'.format(course['id']))
			#course_category_id = course_category_response['primary_category']['id']
			#course_category_name = course_category_response['primary_category']['title']
			
			page = requests.get(database[dictionary_elem]['homepage'])
			soup = BeautifulSoup(page.content, 'html.parser')
			database[dictionary_elem]['prerequisites'] = soup.find_all(class_='requirements__item')[0].get_text()
			expected_learn = soup.find_all(class_='what-you-get__text')
			expected_learn_string = ""
			for i in expected_learn:
				expected_learn_string += i.get_text() + "\n"
			database[dictionary_elem]['expected learning'] = expected_learn_string
			database[dictionary_elem]['time to complete'] = soup.find_all(class_='curriculum-header-length')[0].get_text() 
			database[dictionary_elem]['owner name'] = soup.find_all(class_='instructor__job-title')[0].get_text()

		with open('UdemyDatabaseFile.json', 'w') as myFile:
			json.dump(database, myFile)


		current_url = json_response['next']
		print(current_url)
		json_response = make_response(current_url)


#Reading the file where the database is stored as a dictionary
def read_database_text_file():
	with open('UdemyDatabaseFile.txt', 'rb') as myFile:
		pulledDictionary = pickle.load(myFile)

def read_database_json_file():
	return json.loads(open('UdemyDatabaseFile.json').read())

#Methods for Beautiful Soup
def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

def webpage_exists(webpage):
    c = httplib2.Http()
    response = c.request(webpage, 'HEAD')
    return int(response[0]['status']) < 400









