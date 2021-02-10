# -*- coding: utf-8 -*-

import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CafefCrawlerSpider(newscrawlspider.NewsCrawlSpider):
    name = 'cafef_crawler'
    allowed_domains = ['cafef.vn']
    start_urls = ['http://cafef.vn']

    rules = (Rule(LinkExtractor(allow=(r'.*\.chn',)), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'kinh tế vĩ mô - đầu tư': 'economy', 'thị trường chứng khoán': 'stock',
                      'tài chính - ngân hàng': 'finance', 'tài chính quốc tế': 'finance',
                      'hàng hóa - nguyên liệu': 'goods'}

    def __init__(self, *a, **kwargs):
        super(CafefCrawlerSpider, self).__init__(*a, **kwargs)

        super(CafefCrawlerSpider, self).init_attributes(title_pattern="//h1[contains(@class, 'title')]//text()",
                         summary_pattern="//h2[contains(@class, 'sapo')]//text()",
                         text_pattern="//div[contains(@class, 'content')]//span[contains(@id, 'Content') or contains(@id, 'content')]//p//text()",
                         tag_pattern="//div[contains(@class, 'tag')]//div//a//text()",
                         category_pattern="//div[contains(@class, 'share')]//p//text()",
                         extra_cat_dict=self.extra_cat_dict)
