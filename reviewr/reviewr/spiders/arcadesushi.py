import scrapy
from reviewr.items import ReviewrItem
import json
import pymysql.cursors
from datetime import datetime
import traceback
import sys


class ArcadesushiReviews(scrapy.Spider):
	name = "arcadesushi"


	def start_requests(self):
		urls = ["https://arcadesushi.com/category/reviews/"]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
			

	def parse(self, response):
		links = response.xpath('//article/figure[@class="frameme"]/a/@href').extract()
		
		for link in links:
			url = 'https:' + link
			yield scrapy.Request(url=url, callback=self.parse_contents)


	def check_platform(self, text):
		platforms = ['xbox one x', 'playstation-4', 'ps4', 'xbox-one', 'pc', 'nintendo-3ds', '3ds','wii-u', 'switch', 'android', 'ios', 'ps-vita', 'playstation-vita', 'vita']

		for pl in platforms:
			if pl in text:
				return pl
		return ''


	def parse_contents(self, response):
		item = ReviewrItem()
	
		date = response.xpath('//meta[@name="sailthru.date"]/@content').extract()[0][:10]
		author = response.xpath('//a[@rel="author"]/text()').extract()[0]
		title = response.xpath('//meta[@property="og:title"]/@content').extract()[0]
		name = title.replace(" Review", "")
		conclusion = response.xpath('//meta[@property="og:description"]/@content').extract()[0]
		url = response.xpath('//meta[@property="og:url"]/@content').extract()[0]
		platform = self.check_platform(url)
		score_raw = response.xpath('//meta[@name="sailthru.tags"]/@content').extract()[0]
		score =  score_raw.split()[3][:3].replace('-', '.')
		 
		item['title'] = title
		item['date'] = date
		item['game'] = name
		item['platform'] = platform
		item['author'] = author
		item['url'] = url
		item['score_orig'] = score
		item['score_critic'] = score
		item['conclusion'] = conclusion
		
		print (item)
