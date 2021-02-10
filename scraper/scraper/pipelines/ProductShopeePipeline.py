# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker

class ProductShopeePipeline(object):
    def __init__(self):
        _engine = create_engine("sqlite:///shopee.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _shopee_items = Table("questions", _metadata,
                             Column("id", Integer, primary_key=True),
                             Column("product_id", Text, nullable=False),
                              Column("shop_id", Text, nullable=False))
        _metadata.create_all(_engine)
        Session = sessionmaker(bind=_engine)
        self.session = Session()
        self.connection = _connection
        self.shopee_items = _shopee_items

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            try:
                ins_query = self.shopee_items.insert().values(
                    product_id = item["product_id"],
                    shop_id = item["shop_id"])
                self.connection.execute(ins_query)
            except:
                pass
        return item

    def get_data(self):
        return self.session.query(self.shopee_items)