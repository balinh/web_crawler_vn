from __future__ import division

import math
import scrapy
from scraper.items import TgddListItems
class TgddNet(scrapy.Spider):
    name = "tgdd_list_item"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ProductTgddPipeline.ProductTgddPipeline': 330
        }
    }
    def start_requests(self):
        urls = [
            'https://www.thegioididong.com/dtdd-samsung',
            'https://www.thegioididong.com/dtdd-sony',
            'https://www.thegioididong.com/dtdd-apple-iphone',
            'https://www.thegioididong.com/dtdd-oppo',
            'https://www.thegioididong.com/dtdd-nokia',
            'https://www.thegioididong.com/dtdd-htc',
            'https://www.thegioididong.com/dtdd-asus-zenfone',
            'https://www.thegioididong.com/dtdd-motorola',
            'https://www.thegioididong.com/dtdd-huawei',
            'https://www.thegioididong.com/dtdd-xiaomi',
            'https://www.thegioididong.com/dtdd-mobiistar',
            'https://www.thegioididong.com/dtdd-mobell',
            'https://www.thegioididong.com/dtdd-philips',
            'https://www.thegioididong.com/dtdd-itel',
            'https://www.thegioididong.com/dtdd-vivo',
            'https://www.thegioididong.com/dtdd-bkav'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_items)

    def parse_list_items(self, response):
        lsItems = response.css('.homeproduct > li')
        for data in lsItems:
            reviews = data.css('a > div.ratingresult > span::text')
            if (len(reviews) == 0):
                continue
            product_id = data.css('div:nth-child(2) > button::attr(onclick)').extract()[0]
            product_id = product_id[44:].replace("'", "")
            if (product_id == ''):
                product_id = data.css('a > img::attr(data-original)')
                if (len(product_id) != 0):
                    product_id = product_id.extract()[0].split('/')[6]
                else:
                    continue
            item = TgddListItems()
            item['product_id'] = product_id
            item['number_of_page'] = int(math.ceil(int(reviews.extract()[0].split(' ')[0])/3))
            yield item
