import scrapy

class ReviewrItem(scrapy.Item):
	title = scrapy.Field()
	date = scrapy.Field()
	game = scrapy.Field()
	platform = scrapy.Field()
	author = scrapy.Field()
	url = scrapy.Field()
	score_orig = scrapy.Field()
	score_critic = scrapy.Field()
	conclusion = scrapy.Field()
