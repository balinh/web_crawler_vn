# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class NldCrawlSpider(newscrawlspider.NewsCrawlSpider):
    name = 'nld_crawler'
    allowed_domains = ['nld.com.vn']
    start_urls = ['http://nld.com.vn']

    rules = (Rule(LinkExtractor(allow=(r'.*\.htm')), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'thời sự trong nước': 'news', 'thời sự quốc tế': 'world', 'bạn đọc': 'news', 'công đoàn': 'news',
                      'văn nghệ': 'entertainment',
                      'công nghệ thông tin': 'technology', 'tin tức trong ngày': 'news',
                      'an ninh xã hội': 'legal', 'thời trang hi-tech': 'technology',
                      'tin tài chính - nhà đất - bds': 'finance', 'đời sống showbiz': 'entertainment',
                      'bạn trẻ - cuộc sống': 'live', 'giáo dục - du học': 'education',
                      'ô tô': 'vehicle', 'xe máy - xe đạp': 'vehicle', 'thị trường - tiêu dùng': 'market',
                      'sức khỏe đời sống': 'health'}

    def __init__(self, *a, **kwargs):
        super(NldCrawlSpider, self).__init__(*a, **kwargs)
        super(NldCrawlSpider, self).init_attributes(
                         title_pattern="//h1[contains(@data-field, 'title')]//text()|//div[contains(@class, 'title')]/h1//text()",
                         summary_pattern="//div[contains(@class, 'content')]//h2[contains(@data-field, 'sapo')]//text()|//h2[contains(@class, 'sapo')]//text()",
                         text_pattern="//div[contains(@class, 'content')]//div[contains(@data-field, 'body')]//p//text()|//div[contains(@class, 'contentdetail')]/p//text()",
                         tag_pattern="//div[contains(@class, 'tag')]//li/a/text()|//div[contains(@class, 'keywords')]//a/text()",
                         category_pattern="//div[contains(@class, 'submenu')]//h4/a[contains(@class, 'active')]/@title",
                         extra_cat_dict=self.extra_cat_dict)

    def parse_categories(self, response, xpath_pattern):
        if xpath_pattern == "":
            return ""

        if response.url.find('thitruong.nld.com.vn') != -1:
            return self.categoryDict.get('thi truong', '')
        else:
            return super(NldCrawlSpider, self).parse_categories(response, xpath_pattern)
