from sqlalchemy import create_engine, Table, Column, MetaData, Integer, Text
from scrapy.exceptions import DropItem

class ApiTgddPipeline(object):
    def __init__(self):
        _engine = create_engine("sqlite:///api_tgdd.db")
        _connection = _engine.connect()
        _metadata = MetaData()
        _api_items = Table("questions", _metadata,
                             Column("id", Integer, primary_key=True),
                             Column("rating", Integer, nullable=False),
                             Column("content", Text, nullable=False)
                           )
        _metadata.create_all(_engine)
        self.connection = _connection
        self.api_items = _api_items

    def process_item(self, item, spider):
        is_valid = True
        for data in item:
            if not data:
                is_valid = False
                raise DropItem("Missing %s!" % data)
        if is_valid:
            try:
                ins_query = self.api_items.insert().values(
                    rating = item["rating"],
                    content = item["content"]
                )
                self.connection.execute(ins_query)
            except:
                pass
        return item