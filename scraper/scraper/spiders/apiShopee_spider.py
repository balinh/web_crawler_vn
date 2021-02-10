from __future__ import division
import scrapy
from scraper.items import SingleItems
import json

from scraper.pipelines.ProductShopeePipeline import ProductShopeePipeline


class apiShopee(scrapy.Spider):
    name = "shopee_api"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ApiShopeePipeline.ApiShopeePipeline': 300
        }
    }

    is_check = True

    def start_requests(self):
        infoItem = ProductShopeePipeline()
        regex_url = 'https://shopee.vn/api/v1/comment_list/?item_id={}&shop_id={}&offset={}&limit=100&flag=1&filter=0'
        for info in infoItem.get_data():
            self.is_check = True
            index = 0
            while self.is_check:
                url = regex_url.format(info.product_id,info.shop_id,index)
                yield scrapy.Request(url=url, callback=self.parse_api)
                index = index + 100

    def parse_api(self, response):
        response = json.loads(response.body_as_unicode())
        if (len(response['comments']) == 0):
            self.is_check = False
            return
        for data in response['comments']:
            item = SingleItems()
            item['rating'] = data['rating']
            item['content'] = data['comment']
            yield item