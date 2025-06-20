import asyncio
import aiohttp
from lxml import etree
from openpyxl import Workbook

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# 创建Excel工作簿
wb = Workbook()
ws = wb.active
ws.title = "豆瓣Top250"
ws.append(["电影名称", "评分"])  # 添加表头

# 异步抓取单页数据
async def fetch(session, page):
    url = f'https://movie.douban.com/top250?start={page * 25}&filter='
    async with session.get(url, headers=headers) as response:
        return await response.text()

# 解析HTML并提取数据，写入Excel
def parse(html):
    page = etree.HTML(html)
    lis = page.xpath('//ol/li')
    for li in lis:
        name = li.xpath('.//div[@class="hd"]//a/span/text()')
        score = li.xpath('.//span[@class="rating_num"]/text()')
        ws.append([
            name[0] if name else '',
            score[0] if score else ''
        ])

# 主函数，异步抓取多页
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, i) for i in range(10)]  # 抓取前10页
        pages = await asyncio.gather(*tasks)
        for html in pages:
            parse(html)
    # 保存Excel文件
    wb.save("douban_top250.xlsx")
    print("数据已保存到 douban_top250.xlsx")

# 启动异步任务
if __name__ == '__main__':
    asyncio.run(main())
