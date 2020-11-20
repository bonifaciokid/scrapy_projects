from bs4 import BeautifulSoup
import re

def soup_text(text):
	"""
		Args:
			text: html format
		Returns:
			Cleaned and text only. 
			Empyt string if text is None.
	"""
	if text:
		join_text = ''.join(text)
		soup = BeautifulSoup(join_text, 'html.parser')
		clean_text = soup.get_text().strip()

		return clean_text

	return ''


def remove_non_strings(text):
	"""
		Args: 
			List of strings.
		Return:
			Cleaned and removed new lines and tabs from text
	"""
	words = []
	for string in text:
		if string != '':
			word = string.replace('\n', '').replace('\t', '').replace('\r', '')
			words.append(word)

	return words


def find_string_by_patterns(text, first_pattern, second_pattern):
	"""
		Args:
			first_pattern: string before the desired string
			second_pattern: string after the desired string
		Return
	"""
	form_pattern = first_pattern + "(.*?)" + second_pattern
	find_string = re.findall(form_pattern, raw_str)
	if find_string:
		return ''.join(find_string).strip()

	return ''
