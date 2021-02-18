import scrapy 

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	start_urls = [
		'https://www.tablesleague.com/italy/serie_a/#fixtures',
	]

	def parse(self, response):
		matches = ['Finished', 'Not started']
		for quote in response.css('div.row'):
			status = quote.css('div::attr(title)').get()
			if status in matches:
				yield {
					'status': quote.css('div::attr(title)').get(),
					'date': quote.css('div.cell.date::text').get(),
					'team': quote.css('a::text').get().split('-'),
					'final_score': quote.css('strong::text').get(),
					'first_half': quote.css('span::text').get(),
				}

