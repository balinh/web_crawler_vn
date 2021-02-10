import json
import re
import scrapy
from scraper.items import FptListItems


class FptNet(scrapy.Spider):
    name = "fpt_list_item"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ProductFptPipeline.ProductFptPipeline': 330
        }
    }
    def start_requests(self):
        regex_url = 'https://fptshop.com.vn/dien-thoai?sort=gia-cao-den-thap&trang={}'
        for index in range(1, 14):
            url = regex_url.format(index)
            yield scrapy.Request(url=url, callback=self.parse_list_items)

    def parse_list_items(self, response):
        regex = re.compile('dataLayer.push\((\{.*\})\);', re.DOTALL)
        response = response.css('body > script:nth-child(6)').re_first(regex).replace("'","\"")
        last_comma = response.rfind(',')
        newrs = response[:last_comma] + response[last_comma + 1:]
        newrs = json.loads(newrs)
        lsItems = newrs['ecommerce']['impressions']
        for data in lsItems:
            item = FptListItems()
            item['product_id'] = data['id']
            yield item
