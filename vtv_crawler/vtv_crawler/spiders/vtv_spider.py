# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newscrawlspider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class VtvCrawlSpider(newscrawlspider.NewsCrawlSpider):
    name = 'vtv_crawler'
    allowed_domains = ['vtv.vn']
    start_urls = ['http://vtv.vn']

    rules = (Rule(LinkExtractor(allow=(r'.*\.htm',)), callback='parse_news_contents', follow=True),)
    extra_cat_dict = {'trong nước': 'news', 'góc doanh nghiệp': 'company', 'văn hóa - giải trí': 'entertainment', 'góc khán giả': 'entertainment',
                      }

    def __init__(self, *a, **kwargs):
        super(VtvCrawlSpider, self).__init__(*a, **kwargs)
        super(VtvCrawlSpider, self).init_attributes(title_pattern="//h1[@data-field='title']/text()",
                         summary_pattern="//h2[@data-field='sapo']/text()",
                         #text_pattern="//div[@data-field='body']/p/text()",
                         text_pattern="//div[@data-field='body']/p/text()|//div[@data-field='body']/p/i//text()",
                         tag_pattern="//div[@class='news_keyword']/a[@itemprop='keywords']/@title",
                         category_pattern="//p[@class='tenmuc']/a/@title",
                         extra_cat_dict=self.extra_cat_dict)
