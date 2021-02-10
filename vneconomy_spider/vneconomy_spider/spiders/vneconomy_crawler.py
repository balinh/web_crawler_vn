# -*- coding: utf-8 -*-
import scrapy
import sys
from pathlib import Path

sys.path.append(str(Path('.').absolute().parent))

from basecrawler import basenewsspider


class VneconomyCrawlerSpider(basenewsspider.NewsSpider):
    name = 'vneconomy_crawler'
    allowed_domains = ['vneconomy.vn']
    web_link = "http://vneconomy.vn"
    start_urls = [web_link]

    _urls = [web_link + "/timeline/9920/trang-{0}.htm",
             web_link + "/timeline/6/trang-{0}.htm",
             web_link + "/timeline/7/trang-{0}.htm",
             web_link + "/timeline/5/trang-{0}.htm",
             web_link + "/timeline/17/trang-{0}.htm",
             web_link + "/timeline/19/trang-{0}.htm",
             web_link + "/timeline/99/trang-{0}.htm",
             web_link + "/timeline/16/trang-{0}.htm",
             web_link + "/timeline/23/trang-{0}.htm"
             ]

    #extra_cat_dict = {'doanh nhân': 'business', 'cuộc sống số': 'technology', 'xe 360º': 'vehicle'}
    extra_cat_dict = {'thoi-su': 'news', 'tai-chinh': 'finance',
                      'chung-khoan': 'stock', ''
                      'doanh-nhan': 'business', 'dia-oc': 'real estate',
                      'thi-truong': 'market', 'the-gioi': 'world',
                      'cuoc-song-so': 'technology', 'xe-360': 'vehicle'}

    def __init__(self, *a, **kwargs):
        super(VneconomyCrawlerSpider, self).__init__(*a, **kwargs)
        super(VneconomyCrawlerSpider, self).init_attributes(
                        base_urls=self._urls,
                        link_pattern="//div[contains(@class, 'info')]/h3/a/@href",
                        title_pattern="//div[contains(@class, 'content')]//h1[contains(@data-role, 'title')]/text()",
                        summary_pattern="//div[contains(@class, 'content')]/div[contains(@data-role, 'content')]/p[1]/b/text()",
                        text_pattern="((//div[contains(@class, 'content')]/div[contains(@data-role, 'content')]/div)|(//div[contains(@class, 'content')]/div[contains(@data-role, 'content')]/p))//text()",
                        tag_pattern="",
                        #category_pattern="//ul[contains(@class, 'menu')]/li/a[@class='active']/@title",
                        #category_pattern="//ul[contains(@class, 'menutop')]/li/a[contains(@class, 'active')]/text()",
                        category_pattern="//input[@name='hdCat_Url']/@value",
                        start_pageid=1,
                        end_pageid=1200,
                        browsing="pageid",
                        extra_cat_dict=self.extra_cat_dict)


    def parse_paragraphs(self, response, xpath_pattern):
        paraStr = ''
        paragraphs = response.xpath(xpath_pattern).extract()
        if len(paragraphs) != 0:
            paragraphs = [x.strip() for x in paragraphs if len(x.strip()) > 0]
            paragraphs.pop(0)  # remove summary string
            paraStr = " ".join(paragraphs).lower()

        return paraStr