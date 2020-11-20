import scrapy
from reviewr.items import ReviewrItem
import json
from bs4 import BeautifulSoup
import pymysql.cursors
from datetime import datetime
import traceback
import sys


class AppszoomReviews(scrapy.Spider):
	name = "appszoom"
	

	def start_requests(self):
		urls = [
				"https://www.appszoom.com/iphone-apps?with_review=1",
				"https://www.appszoom.com/android-apps?with_review=1"
				]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		links = response.xpath('//h5[@class="app-name ellipsis-block"]/a/@href').extract()
		
		for link in links:
			link_str = link.strip()
			if "game" in link_str:
				url = "https://www.appszoom.com" + link_str
				yield scrapy.Request(url=url, callback=self.parse_contents)
					
			else:
				print ("This is not a review link!!!")
				print (url)
				print ('   ')


	def parse_contents(self, response):
		item = ReviewrItem()
	
		json_data = response.xpath('//script[@type="application/ld+json"]/text()').extract()[1]
		data = json.loads(json_data.replace('\n', ''))
		title = response.xpath('//h2[@class="text-big text-dark text-with-subtitle"]/text()').extract()[0]
		url_raw = response.xpath('//meta[@property="og:url"]/@content').extract()[0]
		url = url_raw
		date = data['datePublished']
		author = data['author']['name']
		score = data['reviewRating']['ratingValue']
		game_name = data['itemReviewed']['name']
		platform = data['itemReviewed']['operatingSystem']

		conclusion_raw =  response.xpath('//div[@itemprop="description"]').extract()[0]
		conclusion_encoded = ''.join(conclusion_raw).encode('utf-8')
		conclusion_soup = BeautifulSoup(conclusion_encoded, 'html.parser')
		conclusion = conclusion_soup.get_text().strip()

		item['title'] = title
		item['date'] = date
		item['game'] = game_name
		item['platform'] = platform
		item['author'] = author
		item['url'] = url
		item['score_orig'] = score
		item['score_critic'] = score
		item['conclusion'] = conclusion
		
		print (item)

