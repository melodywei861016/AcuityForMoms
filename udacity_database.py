import json
import urllib.request
response = urllib.request.urlopen('https://udacity.com/public-api/v0/courses')
json_response = json.loads(response.read())
database = {}

#Adding Udacity courses to the database
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

"""for elem in database.items(): 
    #key is the course name/key (Ex. 'cs101') , value is a dictionary with all its attributes (Ex. {'title': 'Intro to CS', 'level': 'beginner'})
    print (elem)"""

categorized_courses = {}
for track in json_response['tracks']:
    track_name = track['name']
    categorized_courses[track_name] = []
    for course in track['courses']:
        categorized_courses[track_name].append(course)

for elem in categorized_courses.values():
    #key is the subject/track name (Ex. 'Data Science'), value is a list of course names/keys that can be used to reference to their dictionaries using database[course_name]
    for course in elem:
        print (course)
        print (database[course])



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