import requests
from lxml import etree
import ddddocr
from fontTools.ttLib import TTFont
from PIL import Image,ImageFont,ImageDraw
def parser_font(fontfile):
    ocr = ddddocr.DdddOcr(show_ad=False)
    # 修正：使用传入的fontfile参数而非字符串'fontfile'
    font = TTFont(fontfile)
    maps = font.getBestCmap()
    key_maps = {}

    for k, v in maps.items():
        name = chr(k)
        img = Image.new('RGB', (200, 200), color='red')
        draw = ImageDraw.Draw(img)
        # 修正：同样使用fontfile参数
        draw.text(
            xy=(50, 50),
            text=name,
            font=ImageFont.truetype(fontfile, size=100)
        )
        value = ocr.classification(img)
        key_maps[name] = value

    return key_maps
# 获取字体的映射关系
res = parser_font('sxs.woff')
url = 'https://www.shixiseng.com/interns?keyword=python&city=%E5%85%A8%E5%9B%BD&type=intern'
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
}
# 发送请求获取网页源码
response = requests.get(url=url,headers=headers)
# 获取网页的源码内容
html = etree.HTML(response.text)
# 提取包含所有数据的div
divs = html.xpath('//div[@searchtype="intern"]')
for div in divs:
    # 提取岗位名称
    job = div.xpath('.//a[@class="title ellipsis font"]/text()')[0]
    for k,v in res.items():
        job = job.replace(k,v,-1)
    # 提取要抓取得薪资待遇
    money = div.xpath('.//span[@class="day font"]/text()')[0]
    for k,v in res.items():
        money = money.replace(k,v,-1).replace('o','0',-1)
    # 公司名称
    title = div.xpath('.//a[@class="title ellipsis"]/text()')[0]
    print(job,money,title)



