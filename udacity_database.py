import json
import urllib.request
response = urllib.request.urlopen('https://udacity.com/public-api/v0/courses')
json_response = json.loads(response.read())
database = []
for course in json_response['courses']:
    
    dictionary = {}
    dictionary['title'] = course['title']
    dictionary['homepage'] = course['homepage']
    dictionary['short description'] = course['short_summary']
    dictionary['level'] = course['level'] + course['starter'] #course['starter'] tells if the course is a starter course or not (true/false)
    dictionary['prerequisites'] = course['required_knowledge']
    dictionary['expected learning'] = course['expected_learning']
    dictionary['image'] = course['image']
    if course['affiliates'] != []: #some of the courses' affiliates key lead to empty lists
        dictionary['owner name'] = course['affiliates'][0]['name']
    dictionary['time to complete'] = course['expected_duration'] + " " + course[expected_duration_unit]
    dictionary['price'] = degrees['homepage'] #leads to the homepage of the degree 
    dictionary['availablility_status'] = course['full_course_available']
    
    print (course['title'])


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