from consolidate_json import load_data
import itertools

def retrieve_skills(file_name):
	skills = []
	courses = load_data(file_name)

	for value in courses.values():
		#print value.keys()
		subjects = []
		if value.get("subjects"):
			subjects.append(value.get("subjects"))

		for skill in subjects:
			if skill not in skills:
				skills.append(skill)

	skills = list(itertools.chain.from_iterable(skills))

	with open("Skills.txt", "w") as text_file:
		text_file.write(str(skills))


retrieve_skills('MainDatabaseFile.json')