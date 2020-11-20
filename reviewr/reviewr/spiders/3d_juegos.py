import scrapy
from reviewr.items import ReviewrItem
import json
import pymysql.cursors
from datetime import datetime
import traceback
import sys


class Juegos3dReviews(scrapy.Spider):
	name = "3djuegos"


	def start_requests(self):
		url = "https://www.3djuegos.com/novedades/analisis/juegos/0f0f0f0/fecha/"
		yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		links = response.xpath('//h2/a/@href').extract()
		for url in links:
			yield scrapy.Request(url=url, callback=self.parse_contents)


	def check_platform(self, platform):
		lower_pl = ''.join(platform).lower()
		lists = ['ps4', 'pc', 'switch', '3ds', 'wii u', 'xbox one', 'xone', 'xbox 360', 'x360', 'ps3', 'vita']
		for pl in lists:
			if pl in lower_pl:
				return pl
		return ''


	def parse_contents(self, response):
		item = ReviewrItem()
		
		url = response.url
		json_data = response.xpath('//div/script[@type="application/ld+json"]/text()').extract()[1]
		load_data = json.loads(json_data)
		date =load_data['datePublished']
		conclusion = response.xpath('//p[@class="s16 b c3 lh27 fftext mar_rl4"]/text()').extract()[0]
		game_name = response.xpath('//div[@class="dtc vab oh"]/a/strong/text()').extract()[0]
		title = response.xpath('//title/text()').extract()[0].strip()
		author = response.xpath('//a[@rel="author"]/text()').extract()[0]

		raw_platform = response.xpath('//h2[@class="s18 as14_600 n"]/text()').extract()[0]
		platform = self.check_platform(raw_platform)

		raw_score = response.xpath('//div[@id="val_ana_3"]/div[2]/span/text()').extract()[0].strip()
		score = float(raw_score.replace(',', '.'))
		
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

	