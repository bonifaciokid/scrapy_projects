import scrapy
from reviewr.items import ReviewrItem
from bs4 import BeautifulSoup
import json
import pymysql.cursors
from datetime import datetime
import traceback
import sys


class AndroidGuysGameReviews(scrapy.Spider):
	name = "androidguys"


	def start_requests(self):
		link = "https://www.androidguys.com/category/reviews/app-reviews/"
		yield scrapy.Request(url=link, callback=self.parse)


	def parse(self, response):
		links = response.xpath('//h3[@class="entry-title td-module-title"]/a/@href').extract()
		for url in links:
			if '/app-reviews/' in url:
				yield scrapy.Request(url=url, callback=self.parse_contents)
			else:
				print ('This is not a game review link!!!')

	def parse_contents(self, response):
		item = ReviewrItem()
		
		platform = 'android'
		url = response.url
		title = response.xpath('//h1/text()').extract()[0]
		game_name = title
		author = response.xpath('//div[@class="td-post-author-name"]/a/text()').extract()[0]
		date = response.xpath('//span[@class="td-post-date"]/time/@datetime').extract()[0]
		conclusion = response.xpath('//div[@class="td-review-summary-content"]/text()').extract()[0]
		orig_score = float(response.xpath('//div[@class="td-review-final-score"]/text()').extract()[0])
		score = orig_score * 2.0

		item['title'] = title
		item['date'] = date
		item['game'] = game_name
		item['platform'] = platform
		item['author'] = author
		item['url'] = url
		item['score_orig'] = orig_score
		item['score_critic'] = score
		item['conclusion'] = conclusion
		
		print (item)
