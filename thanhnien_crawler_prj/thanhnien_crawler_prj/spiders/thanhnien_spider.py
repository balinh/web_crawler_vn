import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))


from basecrawler import newsspider
# from scrapy.spiders import Rule
# from scrapy.linkextractors import LinkExtractor
import datetime

class ThanhnienSpider(newsspider.NewsSpider):
    name = 'thanhnien_crawler'
    allowed_domains = ['thanhnien.vn']
    web_link="https://thanhnien.vn"
    start_urls = [web_link]

    _urls = (web_link + "/thoi-su/",
                 web_link + "/the-gioi/",
                 web_link + "/van-hoa/",
                 web_link + "/doi-song/",
                 web_link + "/kinh-doanh/",
                 web_link + "/gioi-tre/",
                 web_link + "/giao-duc/",
                 web_link + "/cong-nghe/",
                 web_link + "/suc-khoe/"
                 )

    def __init__(self, *a, **kwargs):
        super(ThanhnienSpider, self).__init__(*a, **kwargs)
        super(ThanhnienSpider, self).init_date_browsing(base_urls=self._urls,
                                 href_pattern="//article//header//h2//@href",
                                 title_pattern="//h1[contains(@class, title)]/text()",
                                 summary_pattern="//div[contains(@id, 'chapeau')]//text()",
                                 text_pattern="(//div[contains(@id, 'body')]/div|//div[contains(@id, 'body')]/p|//div[contains(@id, 'body')]/div/p|//div[contains(@id, 'body')]/div/div)/text()",
                                 tag_pattern="//ul[contains(@class, 'tag')]//li//a//text()",
                                 category_pattern="//meta[contains(@property, 'section')]/@content",
                                 start_date=datetime.date(year=2005, month=5, day=1),
                                 end_date=datetime.date(year=2017, month=11, day=14))

    # def parse(self, response):
    #     yield scrapy.Request(response.url, callback=self.parse_date(response=response), dont_filter=True)
