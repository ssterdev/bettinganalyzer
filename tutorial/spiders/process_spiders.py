from quotes_spider import QuotesSpider as qs
from scrapy.crawler import CrawlerProcess

def start_process():
	process = CrawlerProcess(settings={
		"FEEDS" : {
			"items.json" : {"format" : "json"},
		},
	})

	process.crawl(qs)
	process.start()