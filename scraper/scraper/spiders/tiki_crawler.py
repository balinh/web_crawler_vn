# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class TikiCrawlerSpider(CrawlSpider):
    name = 'tiki_crawler'
    allowed_domains = ['tiki.vn']
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.EarpodPipeline.EarPodPipeline': 310
        }
    }
    start_urls = [
        'https://tiki.vn/thiet-bi-kts-phu-kien-so'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'\?src=mega-menu'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        questions = response.css('div.product-item')
        for question in questions:
            item = {}
            item['product_id'] = question.css('a::attr(data-id)').extract()[0]
            item['review'] = question.css('.review::text').extract()[0]
            item['link'] = question.css('a::attr(href)').extract()[0]
            yield item
