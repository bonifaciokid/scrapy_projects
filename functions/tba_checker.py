"""
	Check TBA types
"""

import re
from datetime import datetime


#pylint: disable=bad-indentation
def clean_release_date(raw_date):
	"""
		Return cleaned released date by removing not needed string for formatting.
		NOTE: Function only be used if date doesn't fit the date format.
	"""
	raw_date = raw_date.lower()
	filters = ['nd', 'ust', 'st', 'th', 'rd', ',', '.']
	for string in filters:
		if string in raw_date:
			raw_date = raw_date.replace(string, '')

	return raw_date.capitalize()


def is_tba(raw_release_date):
	"""
		Return:
			0: pass date formatting
			1: if can't convert date format
	"""
	cleaned_date = clean_release_date(raw_release_date)
	try:
		try:
			datetime.strptime(cleaned_date, '%b %d %Y')
			return 0
		except ValueError as ve:
			print (ve)

		try:
			datetime.strptime(cleaned_date, '%B %d %Y')
			return 0
		except ValueError as ve:
			print (ve)

		try:
			datetime.strptime(raw_release_date, '%m/%d/%Y')
			return 0
		except ValueError as ve:
			print (ve)

	except Exception:
		return 1

def tba_type(tba, raw_release_date):
	"""
		Args:
			tba: return from is_tba() function
			raw_release_date: raw string release date
		Return:
			0 : if not TBA
			1 : if quarter release
			2 : if season release
			3 : if month release
	"""
	if tba == 0:
		return 0

	quarters = ['q1', '1q', 'quarter 1', 'quarter1', 'first quarter', '1st quarter', 'q2', '2q', 'quarter 2', 'second quarter', '2nd quarter', 'q3', '3q', 'quarter 3', 'third quarter', '3rd quarter', 'q4', '4q', 'quarter 4', 'fourth quarter' , '4th quarter', 'quarter']
	seasons = ['spring', 'fall', 'summer', 'winter', 'autumn']
	months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
	add_data_types = quarters + seasons + months
	check_type = [item for item in add_data_types if item in raw_release_date.lower()]
	if check_type:
		raw_type = check_type[0]
		if raw_type in quarters:
			return 1
		if raw_type in seasons:
			return 2
		if raw_type in months:
			return 3
	return 0


def tba_year(tba, raw_release_date):
	"""
		Args:
			tba: return from is_tba() function
			raw_release_date: raw string release date
		Return:
			If year format exists and current year as default.
	"""
	if tba == 0:
		return 0

	find_year = re.findall(r'\d+', raw_release_date)
	if find_year:
		for year in find_year:
			if len(str(year)) == 4:
				return year
	return 0


def tba_quarter(tba, type_tba, raw_release_date):
	"""
		Args:
			tba: return from is_tba() function
			type_tba: return form tba_type() function
			raw_release_date: raw string release date
		Return:
			1: first quarter release
			2: second quarter release
			3: third quarter release
			4: fourth quarter release
			1-12: if type_tba is 3
	"""
	lower_date = raw_release_date.lower()
	if tba == 0 or type_tba == 0:
		return 0

	if type_tba in (1, 2):
		first_quarter = ['1q', 'winter', 'q1', 'first quarter', '1st quarter', 'quarter 1']
		second_quarter = ['2q', 'q2', 'quarter 2', 'second quarter',  'spring', '2nd quarter']
		third_quarter = ['3q', 'q3', 'quarter 3', 'third quarter', 'summer', '3rd quarter']
		fourth_quarter = ['4q', 'q4', 'quarter 4', 'fourth quarter', 'fall', '4th quarter', 'autumn']
		add_quarters = first_quarter + second_quarter + third_quarter + fourth_quarter
		checked_quarter = [quarter for quarter in add_quarters if quarter in lower_date]
		if checked_quarter:
			quarter = checked_quarter[0]
			if quarter in first_quarter:
				return 1
			if quarter in second_quarter:
				return 2
			if quarter in third_quarter:
				return 3
		return 4
	return month_released(raw_release_date)


def month_released(raw_release_date):
	"""
		Return month index
	"""
	months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
	for indx,month in enumerate(months):
		if month in raw_release_date.lower():
			return indx + 1
	return 12
