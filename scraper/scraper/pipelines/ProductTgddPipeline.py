# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker

class ProductTgddPipeline(object):
    def __init__(self):
        _engine = create_engine("sqlite:///tgdd.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _tgdd_items = Table("questions", _metadata,
                             Column("id", Integer, primary_key=True),
                             Column("product_id", Text, nullable=False),
                              Column("number_of_page", Integer, nullable=False))
        _metadata.create_all(_engine)
        Session = sessionmaker(bind=_engine)
        self.session = Session()
        self.connection = _connection
        self.tgdd_items = _tgdd_items

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            try:
                ins_query = self.tgdd_items.insert().values(
                    product_id = item["product_id"],
                    number_of_page = item["number_of_page"])
                self.connection.execute(ins_query)
            except:
                pass
        return item

    def get_data(self):
        return self.session.query(self.tgdd_items)