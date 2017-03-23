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
    dictionary['level'] = course['level']
    dictionary['prerequisites'] = course['required_knowledge']
    dictionary['expected learning'] = course['expected_learning']
    dictionary['image'] = course['level']
    dictionary['owner name'] = course['affiliates']['name'] #not sure if this works
    dictionary['time to complete'] = course['expected_duration'] + " " + course[expected_duration_unit]
    dictionary['price'] =  



    print (course['title'])
    print (course['homepage'])


The important data that we need: title
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
time frame when you can follow the course (some courses are not always available)