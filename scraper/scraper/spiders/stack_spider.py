import scrapy
from scrapy.selector import Selector
from scraper.items import ScraperItem

class StackSpider(scrapy.Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]
    # def start_requests(self):
    #     urls = [
    #         "https://stackoverflow.com/questions?pagesize=50&sort=newest",
    #     ]
    #     headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    #     for url in urls:
    #         yield scrapy.Request(url=url, headers = headers, callback=self.parse)

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')
        for question in questions:
            item = ScraperItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item
