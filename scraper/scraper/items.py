# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    pass

class TikieListItems(scrapy.Item):
    product_id = scrapy.Field()
    review = scrapy.Field()
    # link = scrapy.Field()
    pass

class DoubleItems(scrapy.Item):
    rating = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    pass

class ShopeeListItems(scrapy.Item):
    product_id = scrapy.Field()
    shop_id = scrapy.Field()
    pass

class SingleItems(scrapy.Item):
    rating = scrapy.Field()
    content = scrapy.Field()
    pass

class TgddListItems(scrapy.Item):
    product_id = scrapy.Field()
    number_of_page = scrapy.Field()
    pass

class FptListItems(scrapy.Item):
    product_id = scrapy.Field()
    pass