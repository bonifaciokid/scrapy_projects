import scrapy
from reviewr.items import ReviewrItem
from bs4 import BeautifulSoup
import json


class AdventureGamerReviews(scrapy.Spider):
	name = "adventuregamers"


	def start_requests(self):
		url = "https://adventuregamers.com/articles/reviews"
		yield scrapy.Request(url, callback=self.parse)


	def parse(self, response):
		links = response.xpath('//h2/a/@href').extract()
		domain = "https://adventuregamers.com"
		for link in links:
			url = domain + link
			yield scrapy.Request(url=url, callback=self.parse_contents)


	def parse_contents(self, response):
		item = ReviewrItem()
		
		data = response.xpath('//script[@type="application/ld+json"]/text()').extract()
		for info in data:
			if 'reviewRating' in info:
				load_info = json.loads(info)
				orig_score = float(load_info['reviewRating']['ratingValue'])
				score = orig_score * 2.0
				url = response.url
				title = response.xpath('//h1/text()').extract()[0].strip()
				game_name = title
				author = response.xpath('//div[@class="pageheader_byline"]/address/a/text()').extract()[0]
				date = response.xpath('//meta[@property="article:published_time"]/@content').extract()[0]

				raw_platform = response.xpath('//div[@class="categories_display"]/span/@tooltip').extract()
				platform = ', '.join(raw_platform)

				raw_conclusion = response.xpath('//div[@class="review_box our_verdict"]/p').extract()[0]
				soup_con = BeautifulSoup(raw_conclusion, 'html.parser')
				conclusion = soup_con.get_text().strip() 

				item['title'] = title
				item['date'] = date
				item['game'] = game_name
				item['platform'] = platform
				item['author'] = author
				item['url'] = url
				item['score_orig'] = orig_score
				item['score_critic'] = score
				item['conclusion'] = conclusion
				item['pub_id'] = 188
				item['assign_to'] = 2
				item['content'] = None

				print (item)
