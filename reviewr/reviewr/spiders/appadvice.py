import scrapy
from reviewr.items import ReviewrItem
import re
from bs4 import BeautifulSoup 
from datetime import datetime
import pymysql.cursors
import json
import traceback
import sys


class AppAdviceReview(scrapy.Spider):
	name = 'app-advice'


	def start_requests(self):
		url = "https://appadvice.com/reviews"
		yield scrapy.Request(url=url, callback=self.parse)


	def parse(self, response):
		urls = response.xpath('//div[@class="aa_gd_e"]/a/@href').extract()
		raw_site = "https://appadvice.com"
		for link in urls[:20]:
			url = raw_site + link
			yield scrapy.Request(url=url, callback=self.parse_contents)


	def parse_contents(self, response):
		item = ReviewrItem()
	
		title = response.xpath('//title/text()').extract()[0]
		author = response.xpath('//a[@class="underline aa_text--bold"]/text()').extract()[0]
		date_raw = response.xpath('//div[@class="aa_text--center aa_opacity--05 aa_margin-t--5"]/text()').extract()[0]
		date = datetime.strptime(date_raw, '%B %d, %Y')

		score = response.xpath('//div[@class="r_c_rt_t_a"]/text()').extract()[0]
		game_name = response.xpath('//div[@class="r_c_rf-app_img aa_position--relative"]/img/@alt').extract()[-1]
		url = response.url
		platform = 'ios'
		
		conclusion_raw = response.xpath('//section[@id="top"]/div[5]/div[2]/div/p').extract()
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

