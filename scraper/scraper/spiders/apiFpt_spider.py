from __future__ import division

import scrapy
from scraper.items import SingleItems
from scraper.pipelines.ProductFptPipeline import ProductFptPipeline
import json
from scrapy.http import HtmlResponse

class apiTgdd(scrapy.Spider):
    name = "fpt_api"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ApiFptPipeline.ApiFptPipeline': 300
        }
    }

    is_check = True

    def start_requests(self):
        infoItem = ProductFptPipeline()
        regex_url = 'https://fptshop.com.vn/Ajax/Product/GetProductReviewMappingDetail?productid={}&page={}&pagesize=4&order=1&v=1'
        for info in infoItem.get_data():
            self.is_check = True
            index = 1
            while self.is_check:
                url = regex_url.format(info.product_id, index)
                yield scrapy.Request(url=url, callback=self.parse_api)
                index = index + 1

    def parse_api(self, response):
        content = json.loads(response.body_as_unicode())
        if content['total'] <= 0 or content['totalRest'] <= -4:
            self.is_check = False
            return
        data = content['view']
        htmlRes = HtmlResponse(url="my HTML string", body=data.encode('utf8'))
        lstComments = htmlRes.css('div.fs-dttrateitem')
        for rc in lstComments:
            item = SingleItems()
            rts = rc.css("div.fs-dttrate > ul > li > span[class='fs-dttr10']")
            item['rating'] = len(rts)
            item['content'] = rc.css('div.fs-dttrtxt::text').extract()[0]
            yield item