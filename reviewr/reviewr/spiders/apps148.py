import scrapy
from reviewr.items import ReviewrItem
from bs4 import BeautifulSoup 
from datetime import datetime
import json
import pymysql.cursors
import traceback
import sys


class Apps148Reviews(scrapy.Spider):
	name = "148apps"


	def start_requests(self):
		url = "https://www.148apps.com/category/reviews/"
		yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		links = response.xpath('//h2/a/@href').extract()

		for link in links:
			url = "https://www.148apps.com" + link
			yield scrapy.Request(url=url, callback=self.parse_contents)


	def change_date(self, date):
		date_raw = date.strip().replace('on ', '').replace('th', '').replace('rd', '').replace('st', '').replace('nd', '').replace('Augu', 'August')
		final = datetime.strptime(date_raw, '%B %d, %Y' )
		return str(final)[0:10] 


	def parse_contents(self, response):
		item = ReviewrItem()
		
		title = response.xpath('//h1/a/text()').extract()[0]
		author = response.xpath('//div[@class="postedby"]/a/text()').extract()[0]
		game_name = title.replace('review', '').replace('Review', '')
		platform = 'ios'
		url = response.url

		conclusion_raw = response.xpath('//div[@class="body clearfloat"]/p').extract()[-1]
		encode_conclusion = ''.join(conclusion_raw)
		soup_conclusion = BeautifulSoup(encode_conclusion, 'html.parser')
		conclusion = soup_conclusion.get_text().strip()

		date_raw = response.xpath('//div[@class="postedby"]/text()').extract()[-1]
		date = self.change_date(date_raw)

		score_raw = response.xpath('//span[@class="rating"]/img/@src').extract()
		join_score = ''.join(score_raw)
		star = float(join_score.count('/star.png'))
		half = float(join_score.count('/halfstar.png') / 2.0)
		orig_score = star + half
		score = (star + half) * 2.0
		
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

