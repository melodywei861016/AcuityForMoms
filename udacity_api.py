import json
import urllib
import urllib.request
import httplib2
from bs4 import BeautifulSoup

def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

def webpage_exists(webpage):
    c = httplib2.Http()
    response = c.request(webpage, 'HEAD')
    return int(response[0]['status']) < 400

def udacity_course_attributes(course_url, attribute):
    """attributes: time, cost, skill level, description"""
    def adjust_attribute_string():
        nonlocal attribute
        if attribute == 'time':
            attribute = 'Timeline'
        elif attribute == 'cost':
            attribute = 'Course Cost'
        elif attribute == 'skill level':
            attribute = 'Skill Level'
    adjust_attribute_string()
    soup = make_soup(course_url)
    if attribute == 'Timeline' or attribute == 'Course Cost' or attribute == 'Skill Level':
        return time_cost_skill_level_of_course(soup, attribute)
    elif attribute == 'description':
        return description_of_course()
    
def time_cost_skill_level_of_course(soup, attribute):
    for section in soup.findAll('div', {'class':'col'}):
        for header in section.findAll('h6'):
            if header.get_text()==attribute:
                for result in section.findAll('h5'):
                    result = result.get_text().strip()
    return result

def description_of_course(soup):
    for section in soup.findAll('div', {'class':'information__summary'}):
        for paragraph in section.findAll('p'):
            description = paragraph.get_text()
    return description


#Udacity API (loops through all Udacity courses)
response = urllib.request.urlopen('https://udacity.com/public-api/v0/courses')
json_response = json.loads(response.read())
for course in json_response['courses']:
    if webpage_exists(course['homepage']):
        try:
            print(course['title'] + ": " + udacity_course_attributes(course['homepage'], 'time'))
        except UnboundLocalError:
            print ('Different page layout: ' + course['title'] + ' @ ' + course['homepage'])

