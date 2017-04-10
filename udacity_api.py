import json
import urllib.request, requests
import urllib
import httplib2
from bs4 import BeautifulSoup
response = urllib.request.urlopen('https://udacity.com/public-api/v0/courses')
json_response = json.loads(response.read())
database = {}


def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, 'lxml')
    return soupdata

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

    with open('UdacityDatabaseFile.json', 'w') as myFile:
        json.dump(database, myFile)

def test():
    return get_rating(make_soup('https://www.udacity.com/course/predictive-analytics-for-business--nd008'))


def get_rating(soup):
    section = soup.find('div', {'class':'stats__average'})
    result = section.find('span')
    print(result)
    #print(soup.findAll('span', {'data-reviews-avg-rating': ''}))

    #return result

def time_cost_skill_level_of_course(soup, attribute):
    for section in soup.findAll('div', {'class':'col'}):
        for header in section.findAll('h6'):
            if header.get_text()==attribute:
                for result in section.findAll('h5'):
                    result = result.get_text().strip()
    return result

categorized_courses = {}
for track in json_response['tracks']:
    track_name = track['name']
    categorized_courses[track_name] = []
    for course in track['courses']:
        categorized_courses[track_name].append(course)

def display_categorized_courses():
    for category in categorized_courses.values():
        #CATEGORY is a list of all courses that belong under the same subject category
        #For categorized_courses, a key is the subject/track name (Ex. 'Data Science'), a value is a list of course names/keys that can be used to reference to their dictionaries using database[course_name]
        for course in category:
            print (course)
            print (database[course])

def read_database_json_file():
    return json.loads(open('UdacityDatabaseFile.json').read())



"""The important data that we need:
title
homepage
short description
level
prerequisites
expected learning
image 
owner name (what university)
time to complete
price
if free price of the certificate
time frame when you can follow the course (some courses are not always available)"""