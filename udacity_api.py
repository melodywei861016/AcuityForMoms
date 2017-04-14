import json
import urllib.request, requests
import urllib
import httplib2
from bs4 import BeautifulSoup
response = urllib.request.urlopen('https://udacity.com/public-api/v0/courses')
json_response = json.loads(response.read())

#Selenium set up
#Quick tutorial on how to use Selenium: https://www.youtube.com/watch?v=bhYulVzYRng
from selenium import webdriver
chrome_path = r"C:\Users\Celena\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

def make_soup(url):
    """Using BeautifulSoup to read page HTML"""
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, 'lxml')
    return soupdata

database = {}

#Adding Udacity courses to the database
def create_database():
    for course in json_response['courses']:
        dictionary_elem = course['key']
        database[dictionary_elem] = {} #the course's key is the key to the dictionary. Its corresponding value is a dictionary of the course's components (time, cost, etc.)

        database[dictionary_elem]['title'] = course['title']
        database[dictionary_elem]['homepage'] = course['homepage']
        database[dictionary_elem]['short description'] = course['short_summary']
        database[dictionary_elem]['level'] = course['level'] + str(course['starter']) #course['starter'] tells if the course is a starter course or not (true/false)
        database[dictionary_elem]['prerequisites'] = course['required_knowledge']
        database[dictionary_elem]['expected learning'] = course['expected_learning']
        database[dictionary_elem]['image'] = course['image']
        if course['affiliates'] != []: #some of the courses' affiliates key lead to empty lists
            database[dictionary_elem]['owner name'] = course['affiliates'][0]['name']
        database[dictionary_elem]['time to complete'] = str(course['expected_duration']) + " " + course['expected_duration_unit']
        # database[dictionary_elem]['price'] =  
        database[dictionary_elem]['availablility_status'] = course['full_course_available']
        database[dictionary_elem]['rating'] = get_course_ratings(course['homepage'])

        #Getting 'subjects' course attribute
        if webpage_exists(course['homepage']):
            soup = make_soup(course['homepage'])
            container = soup.findAll('script', {'type': 'application/ld+json'})
            if container != []:
                database[dictionary_elem]['subjects'] = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)['subjectOfStudy']

    with open('UdacityDatabaseFile.json', 'w') as myFile:
        json.dump(database, myFile)


def get_course_ratings(url):
        """Using Selenium to retrieve the course ratings from Udacity"""
        driver.get(url)
        try:
            return driver.find_element_by_xpath("""//*[@id="reviews"]/div/div[1]/div/div[1]/span""").text
        except: 
            return 'N/A'

def read_database_json_file():
    return json.loads(open('UdacityDatabaseFile.json').read())

def test():
    for course in json_response['courses']:
        if webpage_exists(course['homepage']):
            soup = make_soup(course['homepage'])
            location = soup.findAll('script', {'type': 'application/ld+json'})
            if location != []:
                dic = soup.findAll('script', {'type': 'application/ld+json'})[0].text
                print (json.loads(dic)['subjectOfStudy'], course['homepage'])
        else:
            print('N/A', course['homepage'])


def webpage_exists(webpage):
    c = httplib2.Http()
    response = c.request(webpage, 'HEAD')
    return int(response[0]['status']) < 400

