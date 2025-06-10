# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class PYGWPipeline:
    def open_spider(self,spider):
        """连接数据库"""
        self.client = pymongo.MongoClient('127.0.0.1',27017)
        self.db = self.client['Scrapy']
        self.pygw = self.db['Python岗位']


    def process_item(self, item, spider):
        if spider.name == 'pygw':
            # 保存数据
            self.pygw.insert_one(dict(item))

    def close_spider(self,spider):
        """断开连接"""
        self.client.close()

