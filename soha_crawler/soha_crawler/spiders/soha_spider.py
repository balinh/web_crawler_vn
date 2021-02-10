# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SohaCrawlSpider(newscrawlspider.NewsCrawlSpider):
    name = 'soha_crawler'
    allowed_domains = ['soha.vn']
    start_urls = ['http://soha.vn']

    rules = (Rule(LinkExtractor(allow=(r'.*\.htm',)), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'sống khỏe': 'health',
                      }

    def __init__(self, *a, **kwargs):
        super(SohaCrawlSpider, self).__init__(*a, **kwargs)
        super(SohaCrawlSpider, self).init_attributes(title_pattern="//h1[contains(@data-field,'title')]/text()",
                         summary_pattern="//div[contains(@class,'body')]//h2[contains(@data-field,'sapo')]/text()",
                         text_pattern="//div[contains(@class,'body')]//div[contains(@data-field,'body')]/p//text()",
                         tag_pattern="//div[contains(@class,'tags')]/h3//text()",
                         category_pattern="//nav[contains(@class,'sub-menu')]/a[1]/@title",
                         extra_cat_dict=self.extra_cat_dict)
