# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker

class ProductFptPipeline(object):
    def __init__(self):
        _engine = create_engine("sqlite:///fpt.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _fpt_items = Table("items", _metadata,
                             Column("id", Integer, primary_key=True),
                             Column("product_id", Text, nullable=False, unique=True))
        _metadata.create_all(_engine)
        Session = sessionmaker(bind=_engine)
        self.session = Session()
        self.connection = _connection
        self.fpt_items = _fpt_items

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            try:
                ins_query = self.fpt_items.insert().values(
                    product_id = item["product_id"])
                self.connection.execute(ins_query)
            except:
                pass
        return item

    def get_data(self):
        return self.session.query(self.fpt_items)