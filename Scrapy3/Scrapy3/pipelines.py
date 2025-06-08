# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class Pipeline58TC:
    def open_spider(self,spider):
        """连接数据库"""
        self.client = pymongo.MongoClient('127.0.0.1',27017)
        # 选择数据库
        scrapy = self.client['Scrapy']
        # 选择集合
        # self.db = scrapy['奔驰二手车']
        self.db2 = scrapy['二手车奔驰']
    def close_spider(self,spider):
        """关闭数据库"""
        self.client.close()
    def process_item(self, item, spider):
        if spider.name == 'a58tc':
            # 将数据保存MongoDB数据库
            # self.db.insert_one(dict(item))
            # ItemAdapter类是专门用来对数据进行处理的
            item = ItemAdapter(item)
            title = item.get('title')
            # print(title)
            res = title.split(' ')
            # print(res)
            result = {
                "品牌":res[0],
                "型号":res[1],
                "配置":res[2]
            }
            self.db2.insert_one(result)
        return item
