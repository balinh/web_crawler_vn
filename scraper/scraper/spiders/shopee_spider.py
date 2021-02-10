import json

import scrapy
from scraper.items import ShopeeListItems
class ShopeeNet(scrapy.Spider):
    name = "shopee_list_item"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ProductShopeePipeline.ProductShopeePipeline': 330
        }
    }
    def start_requests(self):
        urls = [
            'https://shopee.vn/api/v1/search_items/?by=pop&order=desc&newest=0&limit=50&categoryids=1979'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_items)

    def parse_list_items(self, response):
        response = json.loads(response.body_as_unicode())
        for data in response['items']:
            item = ShopeeListItems()
            item['product_id'] = data['itemid']
            item['shop_id'] = data['shopid']
            yield item
        # filename = response.url.split("/")[-1] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # questions = response.css('div.shopee-search-result-view__item-card')
        # for question in questions:
        #     item = ShopeeListItems()
        #     data = question.css('a.shopee-item-card--link::attr(href)').extract()[0].slit('.')
        #     dataLen = len(data)
        #     item['product_id'] = data[dataLen-1]
        #     item['shop_id'] = data[dataLen-2]
        #     item['review'] = question.css('span.shopee-item-card__btn-ratings-count::text').extract()[0]
        #     yield item