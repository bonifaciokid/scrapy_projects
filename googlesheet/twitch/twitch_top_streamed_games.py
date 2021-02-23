import requests
import json
import csv
import boto3
from botocore.client import Config
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class TwitchTopStreamedGames:
	"""
		This code is only for twitch currently top streamed games. Twitch's API will return top streams (min, 20, max=100) based in current viewer count. 
		See docs at https://dev.twitch.tv/docs/api.

	"""

	def __init__(self):
		self.BASE_URL = "https://api.twitch.tv/helix/"
		self.CLIENT_ID = "Client-ID"
		self.HEADERS = {'Client-ID' : self.CLIENT_ID, 'Authorization': "Bearer 'your auth token here'"}
		self.INDENT = 2
		self.QUERY = 'streams?first=100'
		self.BUCKET_NAME = 'Bucket-Name'
		self.WORK_SHEET = 'Sheet-Name'
		self.AWS_ACCESS_KEY = "your access key"
		self.AWS_SECRET_KEY = "your secret key"


	def time_stamp(self):
		"""
			return current timestamp
		"""
		current_time = datetime.datetime.now()
		timestamp = current_time.timestamp()

		return timestamp


	def twitch_top_streamed_games(self):
		"""
			return top 100 streamed videos by viewer count
		"""
		url  = self.BASE_URL + self.QUERY
		response = requests.get(url, headers=self.HEADERS)
		response_json = response.json()
		data = response_json['data']
		game_list = [game['game_name'] for game in data]
		game_names = list(set(game_list))
		print (game_names)
		# print_response = json.dumps(response_json, indent=self.INDENT)

		return data
	

	def sort_top_streams(self, response_data, timestamp):
		"""
			returns sorted and add total viewer and streamer count
		"""
		data = response_data
		unique_games = [game['game_id'] for game in data]
		game_ids = list(set(unique_games))

		final_data = []
		for game_id in game_ids:
			viewer_count = 0
			streamer_count = 0
			game_name = ''
			for info in data:
				if game_id == info['game_id']:
					viewer_count+=info['viewer_count']
					streamer_count+=1
					game_name = info['game_name']
			final_data.append([game_id, game_name, viewer_count, streamer_count, timestamp])

		return final_data


	def file_to_csv(self, data, time_stamp):
		"""
			returns file name that will be used to create csv file to be uploaded to s3 bucket
		"""
		file_name = '{}.csv'.format(time_stamp)
		columns = ['game_id', 'game_name', 'viewer_count', 'streamer_count', 'timestamp']
		with open('csv/' + file_name,'w') as w:
			writer=csv.writer(w)
			writer.writerow(columns)
			for itm in data:
				writer.writerow(itm)

		return file_name


	def upload_to_s3(self, file_name):
		"""
			upload csv file to s3 Bucket
		"""
		directory = 'csv/' + file_name
		print (file_name)
		print ('uploading file to s3 bucket ' , self.BUCKET_NAME)
		s3 = boto3.resource(
								's3',
								aws_access_key_id=self.AWS_ACCESS_KEY,
								aws_secret_access_key=self.AWS_SECRET_KEY,
								config=Config(signature_version='s3v4')
							)
		s3.meta.client.upload_file(directory, self.BUCKET_NAME, file_name, ExtraArgs={"ContentType":'application/csv', "ACL":'public-read'})


	def append_to_gsheet(self, data):
		"""
			appending new scraped data to google sheet
		"""
		credentials = '/home/ojieyam/Desktop/twitch/json/client_credentials.json'
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, scopes=scope)
		client = gspread.authorize(credentials)
		sheet = client.open(self.WORK_SHEET).sheet1
		sheet.append_rows(data)
		print ('new data sheet added...')


if __name__ == "__main__":
	twitch = TwitchTopStreamedGames()
	response_data = twitch.twitch_top_streamed_games()
	if response_data:
		ts = twitch.time_stamp()
		sorted_streams = twitch.sort_top_streams(response_data, ts)
		to_csv = twitch.file_to_csv(sorted_streams, ts)
		twitch.append_to_gsheet(sorted_streams)
		twitch.upload_to_s3(to_csv)
	else:
		print ('No scraped data...')

	print ('Done...')
