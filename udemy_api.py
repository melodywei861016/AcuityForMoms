import requests, json, pickle, urllib, urllib.request
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
	def assign_webscraped_attribute(soup_result):
		if soup_result is None:
			return 'N/A'
		else:
			return soup_result.get_text().strip()

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
			ratings_response = make_response('https://www.udemy.com/api-2.0/courses/{}?fields[course]=avg_rating'.format(course['id']))
			database[dictionary_elem]['rating'] = ratings_response['avg_rating']
			subjects_response = make_response('https://www.udemy.com/api-2.0/courses/{}?fields[course]=primary_subcategory'.format(course['id']))
			if subjects_response['primary_subcategory'] is not None:
				database[dictionary_elem]['subjects'] = [subjects_response['primary_subcategory']['title']]
			else:
				database[dictionary_elem]['subjects'] = []


			#Webscraping code to get the rest of the class attributes
			soup = make_soup(database[dictionary_elem]['homepage'])
			expected_learn = soup.find_all(class_='what-you-get__text')
			expected_learn_string = ""
			for i in expected_learn:
				expected_learn_string += i.get_text() + "\n"
			database[dictionary_elem]['expected learning'] = expected_learn_string

			database[dictionary_elem]['time to complete'] = assign_webscraped_attribute(soup.find(class_='curriculum-header-length'))
			database[dictionary_elem]['owner name'] = assign_webscraped_attribute(soup.find(class_='instructor__job-title'))
			database[dictionary_elem]['prerequisites'] = assign_webscraped_attribute(soup.find(class_='requirements__item'))


		with open('UdemyDatabaseFile.json', 'w') as myFile:
			json.dump(database, myFile)

		current_url = json_response['next']
		print(current_url)
		json_response = make_response(current_url)


def update_database():
	saved_database = read_database_json_file()
	
	#saved_database.update(***CODE***)


	global json_response, current_url
	while 'detail' not in json_response.keys():
		for course in json_response['results']:
			subjects_response = make_response('https://www.udemy.com/api-2.0/courses/{}?fields[course]=primary_subcategory'.format(course['id']))
			saved_database[str(course['id'])].update({'subjects': [subjects_response['primary_subcategory']['title']]})

		current_url = json_response['next']
		print(current_url)
		json_response = make_response(current_url)

	with open('UdemyDatabaseFile.json', 'w') as myFile:
		json.dump(database, myFile)


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
