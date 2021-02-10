# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ZingCrawlerSpider(newscrawlspider.NewsCrawlSpider):
    name = "zing_crawler"
    allowed_domains = ["news.zing.vn"]
    start_urls = ['https://news.zing.vn']

    rules = (Rule(LinkExtractor(allow=(r'news\.zing\.vn\/.*\.html',)), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'xe 360': 'vehicle', 'phim ảnh': 'film', 'sống trẻ': 'life'}

    def __init__(self, *a, **kwargs):
        super(ZingCrawlerSpider, self).__init__(*a, **kwargs)
        super(ZingCrawlerSpider, self).init_attributes(title_pattern="//header[contains(@class, 'header')]/h1/text()",
                         summary_pattern="//p[contains(@class, 'article-summary')]/text()",
                         text_pattern="//div[contains(@class, 'article-body')]/p//text()",
                         tag_pattern="//p[contains(@class, 'article-tags')]/a/text()",
                         category_pattern="//header//nav[@class='categories']//li[not(contains(@class, 'homepage')) and contains(@class, 'current')]/a/text()",
                         extra_cat_dict=self.extra_cat_dict)
