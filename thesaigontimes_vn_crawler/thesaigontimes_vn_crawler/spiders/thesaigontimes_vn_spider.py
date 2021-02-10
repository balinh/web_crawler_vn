# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ThesaigontimesVnCrawlSpider(newscrawlspider.NewsCrawlSpider):
    name = "thesaigontimes.vn_crawler"
    allowed_domains = ["thesaigontimes.vn"]
    start_urls = ['http://www.thesaigontimes.vn/']

    rules = (Rule(LinkExtractor(allow=(r'.*\.html')), callback='parse_news_contents', follow=True),)

    extra_cat_dict = {'tài chính - ngân hàng': 'finance', 'tài chính-ngân hàng': 'finance',
                      'thương mại - dịch vụ': 'commerce', 'thương mại-dịch vụ': 'commerce',
                      'văn hóa - xã hội': 'society', 'văn hóa-xã hội': 'society',
                      'hạ tầng - địa ốc': 'real estate', 'hạ tầng-địa ốc': 'real estate',
                      'phân tích - bình luận': 'world', 'phân tích-bình luận': 'world',
                      'thị trường - doanh nghiệp': 'business', 'thị trường-doanh nghiệp': 'business',
                      'giao thương': 'commerce', 'web giá rẻ': 'sale', 'chuyện làm ăn': 'business',
                      'một vòng doanh nghiệp': 'company', 'dữ liệu doanh nghiệp': 'company',
                      'việc gì? ở đâu?': 'jobs', 'nhà đất': 'real estate', 'dự án': 'real estate',
                      'chuyển động doanh nghiệp': 'real estate',
                      }

    def __init__(self, *a, **kwargs):
        super(ThesaigontimesVnCrawlSpider, self).__init__(*a, **kwargs)
        super(ThesaigontimesVnCrawlSpider, self).init_attributes(
                     title_pattern="//h1//span[contains(@class, 'Title')]/text()",
                     summary_pattern="//div[contains(@id, 'ARTICLEVIEW')]//p[contains(@class, 'Summary')]//text()",
                     text_pattern="//div[contains(@id, 'ARTICLEVIEW')]//span/p/text()",
                     tag_pattern="//meta[@name='keywords']/@content",
                     category_pattern="//td//a[contains(@class, 'ArticleHeader')]/text()",
                     extra_cat_dict=self.extra_cat_dict)

    def parse_tags(self, response, xpath_pattern):
        if xpath_pattern == "":
            return ""

        tagstr = response.xpath(xpath_pattern).extract()

        return tagstr
