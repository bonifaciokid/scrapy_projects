import scrapy
from reviewr.items import ReviewrItem
import pymysql.cursors
from datetime import datetime
import json
from bs4 import BeautifulSoup
import traceback
import sys


class AndroidRundownReviews(scrapy.Spider):
	name = 'android-rundown'


	def start_requests(self):
		url = "http://www.androidrundown.com/category/app-rundown/games/"

		yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		raw_site = "https://appadvice.com"
		review_links = response.xpath('//div[@class="entry clearfix"]/h2/a/@href').extract()

		for url in review_links:
			yield scrapy.Request(url=url, callback=self.parse_contents)


	def parse_contents(self, response):
		item = ReviewrItem()

		url = response.url
		platform = 'Android'
		title = response.xpath('//h1[@class="title"]/text()').extract()[0]
		game_name = title.replace('Review', '').replace('review', '')
		author = response.xpath('//a[@rel="author"]/text()').extract()[0]
		score = float(response.xpath('//div[@class="score"]/text()').extract()[-1])

		raw_date = response.xpath('//p[@class="date"]/span/text()').extract()[0]
		date = datetime.strptime(raw_date.strip(), '%b %d, %Y').date()

		conclusion_raw = response.xpath('//div[@class="entry-content"]/p').extract()[-3:]
		encode_con = ''.join(conclusion_raw).encode('utf-8')
		soup_con = BeautifulSoup(encode_con, 'html.parser')
		conclusion = soup_con.get_text().strip()

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
		