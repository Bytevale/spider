import scrapy
from Scrapy2.items import BaiduNewItem

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=baidu"]

    def parse(self, response):
        divs = response.xpath('//div[@tpl="news-normal"]')
        for div in divs:
            title = div.xpath('.//div/h3/a/@aria-label').get()
            content = div.xpath('.//span[@class="c-font-normal c-color-text"]/@aria-label').get()
            item = BaiduNewItem(title=title,content=content)
            yield item



