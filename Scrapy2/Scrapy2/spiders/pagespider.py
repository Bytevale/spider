import scrapy
from Scrapy2.items import DouBan250

class PagespiderSpider(scrapy.Spider):
    name = "pagespider"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]
    pages = [0]
    def parse(self, response):
        # 提取当前数据
        lis = response.xpath('//ol/li')
        for li in lis:
            # 电影名称
            name = li.xpath('.//div[@class="hd"]/a/span//text()').get()
            item = DouBan250(name=name)
            yield item
        self.pages[0] = self.pages[0] + 25
        next_url = f'https://movie.douban.com/top250?start={self.pages[0]}&filter='
        if self.pages[0] <= 25:
            # 如果需要抓取下一个网页,callback指定解析这个请求的方法
            yield scrapy.Request(url=next_url,callback=self.parse)
