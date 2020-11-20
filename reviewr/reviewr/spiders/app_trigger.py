import scrapy
from reviewr.items import ReviewrItem
from datetime import datetime
import json
import pymysql.cursors
from bs4 import BeautifulSoup
import re
import traceback
import sys


class AppTriggerReviews(scrapy.Spider):
	name = 'apptrigger'


	def start_requests(self):
		url = "https://apptrigger.com/reviews/"
		yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		links_1 = response.xpath('//div[@id="the-mosaic"]/div/a/@href').extract()
		links_2 = response.xpath('//h3[@class="title"]/a/@href').extract()
		links = links_1 + links_2
		for url in links:
			yield scrapy.Request(url=url, callback=self.parse_contents)


	def parse_contents(self, response):
		item = ReviewrItem()
		
		score = float(response.xpath('//h3[@class="letter-grade"]/text()').extract()[0])
		url = response.url
		title = response.xpath('//h1/text()').extract()[0]
		game_name = response.xpath('//h3[@class="actor-name"]/text()').extract()[0]
		author = response.xpath('//a[@class="auth-name"]/text()').extract()[0].strip()
		date = response.xpath('//time/@datetime').extract()[0]

		raw_conclusion = response.xpath('//div[@class="details"]').extract()[0]
		soup_con = BeautifulSoup(raw_conclusion, 'html.parser')
		conclusion = soup_con.get_text().strip()

		raw_pl = ', '.join(response.xpath('//p[@class="speakable-content"]').extract()[:2])
		soup_pl = BeautifulSoup(raw_pl, 'html.parser')
		pl_string = soup_pl.get_text().strip().lower()
		find_pl = re.findall('platform(.*?)version reviewed', pl_string)
		if len(find_pl) == 0:
			find_pl = [pl_string]
		join_pl = ''.join(find_pl)
		platform = ###

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