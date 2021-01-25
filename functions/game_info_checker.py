"""functions used for scrapers"""

def game_status(raw_data):
	""" 
		Check if game is early access or not.
		raw_data type must be string.
	"""
	if 'early access' in raw_data.lower():
		return 5
	if 'canceled' in raw_data.lower():
		return 3
	return 1

def is_in_app(genres):
	""" check if game has in-app purchase """
	join_genres = ', '.join(genres).lower()
	if 'in-app' in join_genres or 'in app' in join_genres:
		return 1
	return 0

def is_free(free):
	""" check if game is free based from scraped data """
	if free is True:
		return 1
	return 0

def is_pc(platform):
	""" check if game if for PC """
	if platform is True:
		return 1
	return 0

def is_indie(genres):
	""" check if game is developed by indie developer """
	join_genres = ','.join(genres).lower()
	if 'indie' in join_genres:
		return 1
	return 0

def remove_non_alpha_numeric(string):
	"""
		Args:
			Any strings.
		Return:
			Remove and join non alpha numeric characters from string.
	"""
	chars = [char.lower() for char in string if char.isalnum()]
	join_chars = ''.join(chars)

	return join_chars

def game_publisher(list_data):
	"""
		Args:
			List of scraped string data from mobile crawlers.
		Return:
			Game publiser
	"""
	raw_data = []
	for itm in list_data:
		if 'More' in itm:
			break
		elif 'Published' in itm:
			raw_data.append(itm)
		else:
			raw_data.append(itm)
	join_raw = ' '.join(raw_data[1:])
	if join_raw[:2] == 'by':
		return join_raw[2:]

	return join_raw

def game_developer(list_data):
	"""
		Args:
			List of scraped string data from mobile crawlers.
		Return:
			Game developer
	"""
	raw_data = []
	for itm in list_data:
		if 'CloseDeveloped' in itm:
			raw_data.append(itm)
		elif len(raw_data) > 0:
			if 'MoreDeveloped' not in itm:
				raw_data.append(itm)
			else:
				break

	join_raw = ' '.join(raw_data[1:])
	if join_raw[:2] == 'by':
		return join_raw[2:]

	return join_raw

def esrb_rating_checker(raw_game_content):
	"""
		Args:
			String with uncleaned game content.
		Return:
			content_id : ids based from admin's specification	
	"""
	esrb_dictionary = {
						"everyone 10+" : 2,
						"rated fo 7+" : 2,
						"mature" : 3,
						"mature 17+" : 3,
						"everyone" : 5,
						"todos" : 5,
						"rated for 3+" : 5,
						"pegi 3" : 5,
						"teen" : 6,
						"adults only" : 7,
						"adolescentes" : 7,
						"pegi 3" : 5,
						"pegi 7" : 2,
						"pegi 12" : 6,
						"pegi 16" : 3,
						"pegi 18" : 7
						}

	for esrb_id in esrb_dictionary:
		if esrb_id in raw_game_content.lower():
			return esrb_dictionary[esrb_id]


###