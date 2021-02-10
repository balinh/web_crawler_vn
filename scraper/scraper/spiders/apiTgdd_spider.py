from __future__ import division

import scrapy
from scraper.items import SingleItems
from scraper.pipelines.ProductTgddPipeline import ProductTgddPipeline


class apiTgdd(scrapy.Spider):
    name = "tgdd_api"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ApiTgddPipeline.ApiTgddPipeline': 300
        }
    }

    def start_requests(self):
        infoItem = ProductTgddPipeline()
        url = 'https://www.thegioididong.com/aj/ProductV4/RatingCommentList/'
        for info in infoItem.get_data():
            for index in range(1, info.number_of_page + 1):
                frmdata = {"page": str(index), "productid": info.product_id}
                yield scrapy.FormRequest(url=url, callback=self.parse_api, formdata = frmdata)

    def parse_api(self, response):
        lstComment = response.css('li[class="par"]')
        for data in lstComment:
            rc = data.css('div.rc')
            item = SingleItems()
            rts = rc.css("span:nth-child(1) > i[class='iconcom-txtstar']")
            item['rating'] = len(rts)
            item['content'] = rc.css('p > i::text').extract()[0]
            yield item