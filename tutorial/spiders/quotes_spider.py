import scrapy
import datetime

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.tablesleague.com/italy/serie_a/#fixtures',
    ]

    def parse(self, response):
        year="-2020"
        yearf="-2021"
        matches = ['Finished', 'Not started']
        for quote in response.css('div.row'):
            status = quote.css('div::attr(title)').get()
            if status in matches:
                if 12 - (int(quote.css('div.cell.date::text').get()[3:5])) < 4 and 12 - (int(quote.css('div.cell.date::text').get()[3:5])) > -1:
                    yield {
                        'status': quote.css('div::attr(title)').get(),
                        'data': datetime.datetime.strptime(quote.css('div.cell.date::text').get()[:5] + year + quote.css('div.cell.date::text').get()[5:], "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M"),
                        'team_1': quote.css('a::text').get().split('-', 1)[0],
                        'team_2' : quote.css('a::text').get().split('-', 1)[1],
                        'final_score_home': quote.css('strong::text').get().split('-', 1)[0],
                        'final_score_away': quote.css('strong::text').get().split('-', 1)[1],
                        'first_half_home': quote.css('span::text').get().split('-', 1)[0].strip("("),
                        'first_half_away': quote.css('span::text').get().split('-', 1)[1].strip(")"),

                    }
                else:
                    yield {
                        'status': quote.css('div::attr(title)').get(),
                        'data': datetime.datetime.strptime(quote.css('div.cell.date::text').get()[:5] + yearf + quote.css('div.cell.date::text').get()[5:], "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M"),
                        'team_1': quote.css('a::text').get().split('-', 1)[0],
                        'team_2' : quote.css('a::text').get().split('-', 1)[1],
                        'final_score_home': quote.css('strong::text').get().split('-', 1)[0],
                        'final_score_away': quote.css('strong::text').get().split('-', 1)[1],
                        'first_half_home': quote.css('span::text').get().split('-', 1)[0].strip("("),
                        'first_half_away': quote.css('span::text').get().split('-', 1)[1].strip(")"),

                    }

