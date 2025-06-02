import requests

# 1,准备请求地址
url = 'https://movie.douban.com/top250'
# 2,准备请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
# 3,发送请求
response = requests.get(url=url,headers=headers)
# 4,获取网页的源码
html = response.text
# ==============通过xpath提取数据=================
# 1,导入lxml 中的 etree
from lxml import etree
# 2,创建一个html文档对象
page = etree.HTML(html)
# 3,提取数据
# 电影名称
names = page.xpath('//div[@class="hd"]//a/span/text()')
# 电影评分
scores = page.xpath('//span[@class="rating_num"]/text()')
# 打印结果
print(f"电影名称：{names},电影评分：{scores}")






