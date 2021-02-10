# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class TienphongCrawlSpider(newscrawlspider.NewsCrawlSpider):
    name = 'tienphong_crawler'
    allowed_domains = ['tienphong.vn']
    start_urls = ['https://www.tienphong.vn']

    rules = (Rule(LinkExtractor(allow=(r'.*\.tpo')), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'xã hội': 'news', 'khỏe 360': 'health', 'giới trẻ': 'youth', 'người lính': 'news'}

    def __init__(self, *a, **kwargs):
        super(TienphongCrawlSpider, self).__init__(*a, **kwargs)
        super(TienphongCrawlSpider, self).init_attributes(
                         title_pattern="//h1[contains(@class, 'headline')]/text()",
                         summary_pattern="//article[contains(@class, 'article')]//p[contains(@class, 'sapo')]/text()",
                         text_pattern="//article[contains(@class, 'article')]//div[contains(@class, 'body')]/p//text()|//article[contains(@class, 'article')]//div[contains(@class, 'body')]/div/text()",
                         tag_pattern="//div[contains(@class, 'tags')]//a/text()",
                         category_pattern="//div[contains(@class, 'breadcrum')]//p[contains(@class, 'cate')]/a/text()",
                         extra_cat_dict=self.extra_cat_dict)
