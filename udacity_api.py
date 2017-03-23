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

#RATINGS, SUBJECTS




#Udacity API (all courses)
response = urllib.request.urlopen('https://udacity.com/public-api/v0/courses')
json_response = json.loads(response.read())
for course in json_response['courses']:
	if webpage_exists(course['homepage']):
		try:
			print(course['title'] + ": " + udacity_course_attributes(course['homepage'], 'time'))
		except UnboundLocalError:
			print ('Different page layout: ' + course['title'] + ' @ ' + course['homepage'])



"""extras"""
def time_of_course():
	soup = make_soup("https://www.udacity.com/course/new-android-fundamentals--ud851")
	for section in soup.findAll('div', {'class':'col'}):
		for header in section.findAll('h6'):
			if header.get_text()=='Timeline':
				for time in section.findAll('h5'):
					time = time.get_text()
	print("time of course:", time)


def cost_of_course():
	#arguments: course webpage, time or cost (to extract the time or cost)
	soup = make_soup("https://www.udacity.com/course/new-android-fundamentals--ud851")
	for section in soup.findAll('div', {'class':'col'}):
		for header in section.findAll('h6'):
			if header.get_text()=='Course Cost':
				for cost in section.findAll('h5'):
					cost = cost.get_text()
	return cost

def skill_level_of_course():
	soup = make_soup("https://www.udacity.com/course/new-android-fundamentals--ud851")
	for section in soup.findAll('div', {'class':'col'}):
		for header in section.findAll('h6'):
			if header.get_text()=='Skill Level':
				for skill in section.findAll('h5'):
					skill = skill.get_text().strip()
	return skill




#GET TIME/LENGTH OF NANODEGREE COURSE
def time_of_nanodegree_course():
	soup = make_soup("https://www.udacity.com/course/robotics-nanodegree--nd209")
	for elem in soup.findAll('li', {'class': 'nd-overview__col'}):
		for title in elem.findAll('h6'):
			if title.get_text()=='Time':
				for time in elem.findAll('h5'):
					time_short = time.get_text()
				for time in elem.findAll('p'):
					time_long = time.get_text()
	print("time_short:", time_short)
	print("time_long:", time_long)


"""
>>> soup = bs.BeautifulSoup(foo)
>>> for table in soup.findAll('table', {'class':'theclass'} ):
...     links=table.findAll('a')"""
