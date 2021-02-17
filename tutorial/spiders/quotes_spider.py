import scrapy 

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	start_urls = [
		'https://www.tablesleague.com/italy/serie_a/#fixtures',
	]

	def parse(self, response):
		for quote in response.css('div.row'):
			yield {
				'status': quote.css('div::attr(title)').get(),
				'date': quote.css('div.cell.date::text').get(),
				'team': quote.css('a::text').get(),
				'final_score': quote.css('strong::text').get(),
				'first_half': quote.css('span.First.half.score::text').get(),
				'win_probability': quote.css('div.cell.odd::text').getall(),
			}
