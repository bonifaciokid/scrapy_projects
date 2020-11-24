import re


def game_genre_category(game_data):
	"""
		Args:
			game_data: Scraped steam game data as dictionary
		Return:
			All game genres and categories.
	"""
	try:
		genres = game_data['genres']
	except KeyError:
		genres = []

	try:
		categories = game_data['categories']
	except KeyError:
		categories = []

	game_themes = genres + categories
	if len(game_themes) > 0:
		get_themes = [theme['description'] for theme in game_themes]
		join_themes = ', '.join(get_themes)
		return join_themes
	return ''

def steam_minimum_requirements(raw_requirement):
	"""
		clean steam game minimum requirements
	"""
	try:
		raw_min = raw_requirement.replace('\n', '').replace('\t', '')
		find_min = re.findall("OS:(.*?)</ul>", raw_min)
		if len(find_min) == 0:
			find_min = re.findall("OS(.*?)</ul>", raw_min)
			if len(find_min) == 0:
				find_min = re.findall(':</strong>(.*?)</ul>', raw_min + '</ul>')
		requirements = '<ul><li><strong>OS:' + find_min[0] + "</ul>"

		return requirements

	except:
		raw_min = raw_requirement.replace('\n', '').replace('\t', '')
		find_min = re.findall('<ul(.*?)</ul>', raw_min)
		replace_min = '<ul>' + find_min[0].replace(' class="bb_ul">', '') +  '</ul>'
		requirements = replace_min

		return requirements


def steam_max_requirements(raw_requirement):
	"""
		clean steam game maximum requirements
	"""
	try:
		raw_max = raw_requirement.replace('\n', '').replace('\t', '') + '</ul>'
		find_max = re.findall("OS:(.*?)</ul>", raw_max)
		if len(find_max) == 0:
			find_max = re.findall("OS(.*?)</ul>", raw_max)
			if len(find_max) == 0:
				find_max = re.findall(':</strong>(.*?)</ul>', raw_max + '</ul>')
		max_req = '<ul><li><strong>OS:' + find_max[0] + "</ul>"

		return max_req

	except:
		raw_max = raw_requirement.replace('\n', '').replace('\t', '') +  '</ul>'
		find_max = re.findall('<ul(.*?)</ul>', raw_max)
		replace_max = '<ul>' + find_max[0].replace(' class="bb_ul">', '') 
		max_req = replace_max

		return max_req


def game_file_size(raw_requirement):
	"""
		Return : Use and convert file size to G (Gigabytes).
	"""
	string_gigabytes = ['hard drive', 'storage', 'hdd', 'hard disk', 'disk space']
	if raw_requirement:
		split_requirement = raw_requirement.split('<strong>')
		for requirement in split_requirement:
			requirement = requirement.lower().replace('+', '').replace('at least', '')
			for size in string_gigabytes:
				if size in requirement and 'gb' in requirement:
					required_space = re.findall(r'\d+', requirement)
					space = float('.'.join(required_space))
					return space * 1000

				if size in requirement and 'mb' in requirement:
					required_space = re.findall(r'\d+', requirement)
					space = float('.'.join(required_space))
					return space * 1
	return 0