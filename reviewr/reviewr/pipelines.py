import datetime
import sys
sys.path.insert(1, '/var/scrapy/functions/')
import db_connections as connection


class ReviewrPipeline(object):

	
	def __init__(self):
		scrapy_db = connection('db_key')
		self.cursor = scrapy_db[0]
		self.conn = scrapy_db[1]
		
		scrapy_logs = connection('log_key')
		self.cursor_logs = scrapy_logs[0]
		self.conn_logs = scrapy_logs[1]
		

	def process_item(self, item, spider):	
		"""
			process item to database, google sheet, etc.
		"""




