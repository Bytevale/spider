"""
需求：爬取车的名称
解法:1，现在items中定义要爬取的信息
2，然后在a58tc中解析数据，
3，返回到管道pipelines中保存
"""
import scrapy
from Scrapy3.items import ESC58Item

class A58tcSpider(scrapy.Spider):
    name = "a58tc"
    allowed_domains = ["cs.58.com"]
    start_urls = ["https://cs.58.com/benchi/?spm=u-2few7p4vh988mb62t1.2few8w827wgt4eurg.kd_309446783953.cr_68762495766.ac_10101461.cd_9091889713907100611&listfrom=dspadvert&utm_source=sem-esc-baidu-pc&PGTID=0d305e5e-0019-eefb-9b3e-a4b4a3db2bda&ClickID=55#mainCon"]

    def parse(self, response):
        # 定位到包含所有数据的元素
        lis = response.xpath('//div[@id="list"]/ul/li')
        for li in lis:
            # 定位到二手车的名称
            title = li.xpath('.//h2//span/text()').getall()
            title = ' '.join(title).strip()
            # print(title)
            item = ESC58Item(title=title)
            # 返回到管道中
            yield item



