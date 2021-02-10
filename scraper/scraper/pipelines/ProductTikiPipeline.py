# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker

class ProductTikiPipeline(object):
    def __init__(self):
        _engine = create_engine("sqlite:///tiki_mobile.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _earpod_items = Table("questions", _metadata,
                             Column("id", Integer, primary_key=True),
                             Column("product_id", Text, unique=True, nullable=False),
                             Column("review", Text, nullable=False))
        _metadata.create_all(_engine)
        Session = sessionmaker(bind=_engine)
        self.session = Session()
        self.connection = _connection
        self.earpod_items = _earpod_items

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            try:
                review_data = item["review"].replace(')','(').replace('(', '').replace(')', '').split(' ')[0]
                if review_data != u'Ch\u01b0a':
                    ins_query = self.earpod_items.insert().values(
                        product_id = item["product_id"],
                        review = review_data)
                    self.connection.execute(ins_query)
            except:
                pass
        return item

    def get_data(self):
        return self.session.query(self.earpod_items)