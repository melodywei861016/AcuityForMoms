import requests, json, pickle
from requests.auth import HTTPBasicAuth
from datetime import datetime
import requests # pip install requests
import urllib
import urllib.request
import httplib2
from bs4 import BeautifulSoup

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

#Selenium set up
#Quick tutorial on how to use Selenium: https://www.youtube.com/watch?v=bhYulVzYRng
from selenium import webdriver
chrome_path = r"C:\Users\Celena\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

def make_soup(url):
	"""Using BeautifulSoup to read page HTML"""
	thepage = urllib.request.urlopen(url)
	soupdata = BeautifulSoup(thepage, "lxml")
	return soupdata

def make_response(url):
	response = requests.get(url, headers=headers)
	json_response = json.loads(response.text)
	return json_response

full_catalog_info =  make_response('https://api.edx.org/catalog/v1/catalogs/')['results'][0]

json_response = make_response('https://api.edx.org/catalog/v1/catalogs/' + str(full_catalog_info['id']) + '/courses')


database = {}
pulledDictionary = {}

#Adding EdX courses to the database
def create_database():
	for course in json_response['results']:
	    dictionary_elem = course['key']
	    database[dictionary_elem] = {} #the course's key is the key to the dictionary. Its corresponding value is a dictionary of the course's components (time, cost, etc.)

	    database[dictionary_elem]['title'] = course['title']
	    database[dictionary_elem]['homepage'] = course['course_runs'][0]['marketing_url']
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
	    database[dictionary_elem]['subjects'] = [course['subjects'][0]['name']] #A list of subjects
	    #database[dictionary_elem]['availablility_status'] = course['full_course_available']

	    database[dictionary_elem]['rating'] = get_course_ratings(course['course_runs'][0]['marketing_url'])
	    
	with open('EdXDatabaseFile.json', 'w') as myFile:
		json.dump(database, myFile)


def get_course_ratings(url):
        """Using Selenium to retrieve the course ratings from EdX"""
        driver.get(url)
        num_reviews = driver.find_element_by_xpath("""//*[@id="course-about-area"]/div[1]/span/a""").text
        if num_reviews == '0 Reviews':
        	return 'N/A'
        return driver.find_element_by_xpath("""//*[@id="course-about-area"]/div[1]/span/span[1]""").text


def update_database():
	saved_database = read_database_json_file()
	
	#saved_database.update(***CODE***)

	with open('EdXDatabaseFile.json', 'w') as myFile:
		json.dump(database, myFile)


def read_database_text_file():
	global pulledDictionary
	with open('EdXDatabaseFile.txt', 'rb') as myFile:
		pulledDictionary = pickle.load(myFile)

def read_database_json_file():
	return json.loads(open('EdXDatabaseFile.json').read())








