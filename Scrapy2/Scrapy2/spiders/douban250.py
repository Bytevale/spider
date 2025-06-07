"""
抓取电影的名称和url地址
进入到电影的详情页面，抓取简介，评价人数

思路：
    1，在管道items里面先定义要抓取的数据
    2，在爬虫里面提取数据，类比requests使用思路就可以
"""
import scrapy
from Scrapy2.items import DouBanDesc250

class Douban250Spider(scrapy.Spider):
    name = "douban250"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]
    pages = [0]

    def parse(self, response):
     """解析数据"""
     # 定位到包含所有元素的标签
     lis = response.xpath('//ol/li')
     # 用for循环遍历lis
     for li in lis:
        # 定位到电影名称
        name = li.xpath('.//div[@class="hd"]/a/span/text()').get()
        # 定位到电影的详情页地址
        url = li.xpath('.//a/@href').get()
        # 将数据保存到字典格式中
        data = {"name":name,"url":url}
        # 将详情页提取到scrapy调度器中
        yield scrapy.Request(url=url,meta=data,callback=self.parse_info_page)

     # 进行自动翻页
     self.pages[0] = self.pages[0] + 25
     next_url = f'https://movie.douban.com/top250?start={self.pages[0]}&filter='
     # 利用if判断设置请求页数
     if self.pages[0] <=75:
        # 如果抓取到下一页，callback解析这个请求方法
        yield scrapy.Request(url=next_url,callback=self.parse)

    def parse_info_page(self,response):
        # 电影的简介
        short = response.xpath('//span[@property="v:summary"]/text()').get()
        # 电影的评价人数
        people = response.xpath('//a[@class="rating_people"]/span/text()').get()
        # 电影的名称
        name = response.meta['name']
        # 电影的详情页地址
        url = response.meta['url']
        item = DouBanDesc250(short=short,people=people,name=name,url=url)
        yield item









