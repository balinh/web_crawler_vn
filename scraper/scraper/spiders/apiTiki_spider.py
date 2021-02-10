from __future__ import division
import scrapy
from scraper.items import DoubleItems
import json
import math

from scraper.pipelines.ProductTikiPipeline import ProductTikiPipeline


class apiTiki(scrapy.Spider):
    name = "tiki_api"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ApiTikiPipeline.ApiTikiPipeline': 300
        }
    }
    def start_requests(self):
        infoItem = ProductTikiPipeline()
        headUrl = 'https://tiki.vn/api/v2/reviews?product_id='
        midUrl = '&limit=5&page='
        tailUrl = '&sort=score|desc,customer|all,stars|all&include=comments'
        for info in infoItem.get_data():
            for index in range(int(math.ceil(int(info.review) / 5))):
                url = headUrl + info.product_id + midUrl + str(index + 1) + tailUrl
                yield scrapy.Request(url=url, callback=self.parse_api)
        # urls = [
        #     'https://tiki.vn/api/v2/reviews?product_id=653140&limit=5&page=1&sort=score|desc,customer|all,stars|all&include=comments'
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse_api)

    def parse_api(self, response):
        response = json.loads(response.body_as_unicode())
        for data in response['data']:
            item = DoubleItems()
            item['rating'] = data['rating']
            item['content'] = data['content']
            item['title'] = data['title']
            yield item