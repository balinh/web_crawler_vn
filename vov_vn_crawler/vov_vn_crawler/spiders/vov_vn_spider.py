# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class VovVnCrawlSpider(newscrawlspider.NewsCrawlSpider):
    name = "vov.vn_crawler"
    allowed_domains = ["vov.vn"]
    start_urls = ['http://vov.vn']

    rules = (Rule(LinkExtractor(allow=(r'.*\.vov')), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'văn hóa - giải trí': 'entertainment', 'ô tô - xe máy': 'vehicle'}

    def __init__(self, *a, **kwargs):
        super(VovVnCrawlSpider, self).__init__(*a, **kwargs)
        super(VovVnCrawlSpider, self).init_attributes(
                     title_pattern="//h1[contains(@class, 'title')]/text()",
                     summary_pattern="//section[contains(@class, 'main-article')]//p[contains(@class, 'sapo')]/text()",
                     text_pattern="//div[contains(@id, 'article-body')]//p//text()",
                     tag_pattern="//meta[@name='keywords']/@content",
                     category_pattern="//ul[contains(@class, 'vov-breadcrumb')]/h2/a/text()",
                     extra_cat_dict=self.extra_cat_dict)

    def parse_tags(self, response, xpath_pattern):
        if xpath_pattern == "":
            return ""

        tagstr = response.xpath(xpath_pattern).extract()

        return tagstr
