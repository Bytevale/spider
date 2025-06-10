import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Scrapy4.items import PYGWItem
# 准备好所有页面的地址
urls = [
    'https://www.shixiseng.com/interns?keyword=python'
]
for i in range(2,4):
    base_url = f'https://www.shixiseng.com/interns?page={i}&type=intern&keyword=python&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend='
    urls.append(base_url)
class PygwSpider(CrawlSpider):
    name = "pygw"
    allowed_domains = ["shixiseng.com"]
    # 启动所有的页面地址为所有的列表页
    start_urls = urls
    # 深度访问页面的url地址提取规则
    rules = (Rule(LinkExtractor(allow=r"https://www.shixiseng.com/intern/.+?pcm=pc_SearchList"), callback="parse_item",
                  follow=True),)

    def parse_item(self, response):
        name = response.xpath('//div[@class="com_intro"]/a[2]/text()').get()
        job = response.xpath('//div[@class="new_job_name"]/span/text()').get()
        gwzz = response.xpath('//div[@class="job_detail"]//text()').getall()
        name = ' '.join(name).replace(' ','').replace('\n','')
        gwzz = ' '.join(gwzz).replace('\n','').replace('\t','')
        item = PYGWItem(name=name,gwzz=gwzz,job=job)
        yield item