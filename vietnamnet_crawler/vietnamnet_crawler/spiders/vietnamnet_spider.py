# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class VietnamnetCrawlSpider(newscrawlspider.NewsCrawlSpider):
    name = "vietnamnet_crawler"
    allowed_domains = ["vietnamnet.vn"]
    start_urls = ['http://vietnamnet.vn']

    rules = (Rule(LinkExtractor(allow=(r'.*\.html',)), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'bạn đọc': 'reader'}

    def __init__(self, *a, **kwargs):
        super(VietnamnetCrawlSpider, self).__init__(*a, **kwargs)
        super(VietnamnetCrawlSpider, self).init_attributes(
                         title_pattern="//h1[contains(@class, 'title')]/text()",
                         summary_pattern="//div[contains(@class, 'ArticleContent')]/p[1]/strong/text()",
                         text_pattern="//div[contains(@class, 'ArticleContent')]/p//text()",
                         tag_pattern="//div[contains(@class, 'tag')]//li/h3//text()",
                         category_pattern="//div[contains(@class, 'CateTitle left')]//a//text()",
                         extra_cat_dict=self.extra_cat_dict)

