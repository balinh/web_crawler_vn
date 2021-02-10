# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Web24hCrawlSpider(newscrawlspider.NewsCrawlSpider):
    name = "web24h_crawler"
    allowed_domains = ["www.24h.com.vn"]
    start_urls = ['http://www.24h.com.vn']

    rules = (Rule(LinkExtractor(allow=(r'.*\.html',)), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'công nghệ thông tin': 'technology', 'tin tức trong ngày': 'news',
                      'an ninh xã hội': 'legal', 'thời trang hi-tech': 'technology',
                      'tin tài chính - nhà đất - bds': 'finance', 'đời sống showbiz': 'entertainment',
                      'bạn trẻ - cuộc sống': 'live', 'giáo dục - du học': 'education',
                      'ô tô': 'vehicle', 'xe máy - xe đạp': 'vehicle', 'thị trường - tiêu dùng': 'market',
                      'sức khỏe đời sống': 'health'}

    def __init__(self, *a, **kwargs):
        super(Web24hCrawlSpider, self).__init__(*a, **kwargs)
        super(Web24hCrawlSpider, self).init_attributes(
                         title_pattern="//div[contains(@class,'baiviet')]//h1[contains(@class,'title')]/text()",
                         summary_pattern="//div[contains(@class,'baiviet')]//h2/p[contains(@class,'sapo')]/text()",
                         text_pattern="//div[contains(@class,'text')]/p/text()|//div[contains(@class,'text')]/p/a/text()|//div[contains(@class,'text')]/p/strong/text()",
                         tag_pattern="//div[contains(@class,'baiviet-sukien')]//a/@title",
                         #category_pattern="//ul[contains(@class, 'breadcrum')]/li/a/@title",
                         category_pattern="//div[contains(@class, 'bread-cum-cm2')]/div[contains(@class, 'breadcum-CMtab')]//ul[contains(@class, 'breadcrum')]/li/a/@title",
                         extra_cat_dict=self.extra_cat_dict)

