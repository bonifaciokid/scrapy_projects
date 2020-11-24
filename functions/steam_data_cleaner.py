import re


def game_genre_category(game_data):
	"""
		Args:
			game_data: Scraped steam game data as dictionary
		Return:
			All game genres and categories.
	"""
	game_themes = game_data['genres'] + game_data['categories']
	get_themes = [theme['description'] for theme in game_themes]
	join_themes = ', '.join(get_themes)

	return join_themes 


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


# raw_req = """<strong>Recommended:</strong><br><ul class="bb_ul"><li><strong>OS:</strong> Windows® 8.1 / 10 64-bit<br></li><li><strong>Processor:</strong> AMD Ryzen™ 3 1200 / Intel® Core™ i5 2.5GHz<br></li><li><strong>Memory:</strong> 8 GB RAM<br></li><li><strong>Graphics:</strong> AMD Radeon™ RX 470 / NVIDIA® GeForce® GTX 1050 Ti<br></li><li><strong>DirectX:</strong> Version 11<br></li><li><strong>Storage:</strong> 20 GB available space<br></li><li><strong>Additional Notes:</strong> 60 FPS @ 1920x1080</li></ul>"""

# size = game_file_size(raw_req)
# print (size)