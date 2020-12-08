"""
	Conver raw release date to 'YYYY-mm-dd' format
"""

import re
from datetime import datetime, date

#pylint: disable=bad-indentation
#pylint: disable=no-self-use
class ReleaseDateConverter:
	"""
		Clean, check and convert scraped released date to db date format.
	"""
	def season_released(self, raw_date):
		"""
			Returns equivalent month for each seasons.
			NOTE: Function only be used if date doesn't fit the date format.
		"""
		seasons = ['fall', 'autumn', 'summer', 'winter', 'spring', 'mid']
		for season in seasons:
			if season in raw_date.lower():
				if season in ('fall', 'autumn'):
					return 'nov'
				if season == 'summer':
					return 'aug'
				if season == 'winter':
					return 'feb'
				if season == 'spring':
					return 'may'
				if season == 'mid':
					return 'jun'
		return 'dec'
		

	def month_release(self, raw_date):
		"""
			Returns equivalent month from raw_date, season or quarter release.
			NOTE: Function only be used if date doesn't fit the date format.
		"""
		lower_date = raw_date.lower()
		month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
		for month in month_list:
			if month in lower_date:
				return month

		first = ['jan', 'feb', 'mar', 'q1', 'quarter 1', 'quarter1', '1q', 'first quarter']
		second = ['apr', 'may', 'jun', 'q2', 'quarter 2', 'quarter2', '2q', 'second quarter']
		third = ['jul', 'aug', 'sep', 'q3', 'quarter 3', 'quarter3', '3q', 'third quarter']
		fourth = ['oct', 'nov', 'dec', 'q4', 'quarter 4', 'quarter4', '4q', 'fourth quarter']
		add_quarters = first + second + third + fourth
		month = [month for month in add_quarters if month in lower_date]
		if month:
			raw_month = month[0]
			if raw_month in first:
				return 'mar'
			if raw_month in second:
				return 'jun'
			if raw_month in third:
				return 'sep'
			return 'dec'
		return self.season_released(lower_date)


	def year_release(self, raw_date):
		"""
			Return year released if any or return current year.
			NOTE: Function only be used if date doesn't fit the date format.
		"""
		lower_date = raw_date.lower()
		find_year = re.findall(r'\d+', lower_date)
		now = datetime.now()
		year_now = now.year

		if find_year:
			for year in find_year:
				if len(str(year)) == 4:
					return str(year)
		return str(year_now)


	def find_release_date(self, raw_date, month, quarter_check, year):
		"""
			Return last date of the month based on month and quarter object.
			NOTE: Function only be used if date doesn't fit the date format.
		"""
		lower_raw_date = raw_date.lower()
		month_31 = ['jan', 'mar', 'may', 'jul', 'aug', 'oct', 'dec']
		find_date = re.findall(r'\d+', lower_raw_date)
		if find_date:
			if quarter_check == 0:
				for rdate in find_date:
					if int(rdate) <= 31:
						return str(rdate)
		if month == 'feb':
			if int(year[-2:]) % 4 == 0:
				return '29'
			return '28'
		if month in month_31:
			return '31'
		return '30'


	def quarter_release(self, raw_date):
		"""
			Return last date of the month based on month and quarter object.
			NOTE: Function only be used if date doesn't fit the date format.
		"""
		lower_raw_date = raw_date.lower().replace(' ', '')
		quarters = ['q1', 'q2', 'q3', 'q4', '1q', '2q', '3q', '4q', 'quarter1', 'quarter2', 'quarter3', 'quarter4']
		for quarter in quarters:
			if quarter in lower_raw_date:
				return 1
		return 0


	def clean_release_date(self, raw_date):
		"""
			Return cleaned released date by removing not needed string for formatting.
			NOTE: Function only be used if date doesn't fit the date format.
		"""
		raw_date = raw_date.lower()
		filters = ['nd', 'ust', 'st', 'th', 'rd', ',', '.']
		for string in filters:
			if string in raw_date:
				raw_date = raw_date.replace(string, '')

		return str(raw_date.capitalize().encode('ascii', 'ignore'))


	def format_date(self, coming_soon, raw_date, status, tba):
		"""
			Return converted date (format: 2020-12-31).
		"""
		cleaned_date = self.clean_release_date(raw_date)
		if tba == 0:
			
				try:
					release_date = datetime.strptime(cleaned_date, '%b %d %Y')
					return release_date
				except ValueError as ve:
					print (ve)

				try:
					release_date = datetime.strptime(cleaned_date, '%B %d %Y')
					return release_date
				except ValueError as ve:
					print (ve) 

				try:
					release_date = datetime.strptime(raw_date, '%m/%d/%Y')
					return release_date
				except ValueError as ve:
					print (ve)

		year = self.year_release(cleaned_date)
		check_quarter = self.quarter_release(cleaned_date)
		month = self.month_release(cleaned_date)
		rdate = self.find_release_date(cleaned_date, month, check_quarter, year)
		added_date_data = month + ' ' + rdate + ' ' + year
		release_date = datetime.strptime(added_date_data, '%b %d %Y').date()

		if status == 5:
			return release_date

		date_now = datetime.now().date()
		if coming_soon is True:
			if release_date < date_now:
				print ('coming soon!!!')
				now = datetime.now()
				year_now = now.year
				return date(year_now, 12, 31)
			return release_date
		return release_date
