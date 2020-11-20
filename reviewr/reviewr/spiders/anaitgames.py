import scrapy
from reviewr.items import ReviewrItem
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import sys


class AnaitGameReviews(scrapy.Spider):
	name = "anait-games"


	def start_requests(self):
		url = "https://www.anaitgames.com/analisis"
		yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		links = response.xpath('//div[@class="post"]/h2/a/@href').extract()
		for url in links:
			yield scrapy.Request(url=url, callback=self.parse_contents)


	def parse_contents(self, response):
		item = ReviewrItem()
		
		url = response.url
		title = response.xpath('//h2[@itemprop="name"]/text()').extract()[0]
		date = response.xpath('//meta[@itemprop="datePublished"]/@content').extract()[0][0:10]
		score = response.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]
		game_raw = title.encode('ascii', 'ignore').decode('utf8')
		game_name = game_raw.replace('Anlisis de ', '')

		author_raw = response.xpath('//span[@itemprop="author"]/span/text()').extract()
		if len(author_raw) == 0:
			author_raw = response.xpath('//span[@class="author"]/text()').extract()
		author = author_raw[0]

		platform_raw = response.xpath('//div[@class="header"]/p/a/text()').extract()
		platform = #function

		item['title'] = title
		item['date'] = date
		item['game'] = game_name
		item['platform'] = platform
		item['author'] = author
		item['url'] = url
		item['score_orig'] = score
		item['score_critic'] = score
		item['conclusion'] = None
		
		print (item)
