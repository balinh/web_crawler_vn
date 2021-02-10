# -*- coding: utf-8 -*-
import scrapy
from vnexpress_spider.items import VnexpressCrawlerItem
from scrapy.selector import HtmlXPathSelector


class VnexpressCrawler(scrapy.Spider):
    allowed_domains = ['https://vnexpress.net']
    categoryDict = {'thời sự': 'news', 'thế giới': 'world', 'kinh doanh': 'business', 'giải trí': 'entertainment',
                    'thể thao': 'sport', 'pháp luật': 'legal', 'giáo dục': 'education', 'gia đình': 'family',
                    'du lịch': 'travel', 'khoa học': 'science', 'số hóa': 'technology', 'xe': 'vehicle', 'cộng đồng': 'community'}

    def __init__(self, begin_urls, npage):
        self.start_urls = [begin_urls]
        self.npage = npage
        for page in range(2, npage + 1):
            self.start_urls.append(self.begin_urls + '/page/' + str(page) + ".html")

    def parse(self, response):
        for href in response.xpath("//h3[contains(@class, 'title_news')]/a//@href"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_news_contents, dont_filter=True)

    def parse_news_contents(self, response):
        item = VnexpressCrawlerItem()

        paragraphs = response.xpath("//p[contains(@class, 'Normal')]/descendant::text()").extract()

        if len(paragraphs) != 0:
            item['url'] = response.url
            item['title'] = response.xpath("//h1[contains(@class, 'title_news_detail mb10')]/descendant::text()").extract()[
                0].strip()

            item['summary'] = response.xpath("//h2[contains(@class, 'description')]/descendant::text()").extract()[
                0].strip()

            paragraphs = [x.strip() for x in paragraphs if len(x.strip()) > 0]
            item['text'] = item['title'] + ". " + " ".join(paragraphs)

            tags = response.xpath("//div[contains(@class, 'block_tag')]//h5/a/@title").extract()
            if len(tags) != 0:
                item['tags'] = ";".join([tag.strip() for tag in tags])
            else:
                item['tags'] = ""

            #item['category'] = response.xpath("//meta[@itemprop='articleSection']/@content").extract()
            #category = response.xpath("//li[@class='start']//a//text()").extract()[0].strip()
            categories = response.xpath("//ul[start-with(@class,'breadcrumb']//h4/a//text()").extract()

            if len(categories) > 0:
                item['category'] = self.categoryDict.get(categories[0].strip().lower(), '')
                if len(categories) > 1:
                    cat = self.categoryDict.get(categories[1].strip().lower(), '')
                    if cat != '':
                        item['category'] += ',' + cat

            yield item




