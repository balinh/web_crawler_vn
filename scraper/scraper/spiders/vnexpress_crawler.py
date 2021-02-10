# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scraper.items import ScraperItem


class VnexpressCrawlerSpider(CrawlSpider):
    name = 'vnexpress_crawler'
    allowed_domains = ['vnexpress.net']
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ScraperPipeline': 300
        }
    }
    start_urls = ['https://thethao.vnexpress.net/']

    rules = (
        Rule(LinkExtractor(allow=r'/page/[0-5].html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # questions = response.xpath('//article[@class="list_news"]/h3')
        questions = response.css('.list_news h3')
        for question in questions:
            item = ScraperItem()
            item['title'] = question.css('a::text').extract()[0]
            item['url'] = question.css('a::attr(href)').extract()[0]
            yield item
