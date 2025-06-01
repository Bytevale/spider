import requests
from lxml import etree
import ddddocr
from fontTools.ttLib import TTFont
from PIL import Image, ImageFont, ImageDraw
from pymongo import MongoClient

# MongoDB配置
MONGO_URI = 'mongodb://localhost:27017/'  # 根据你的MongoDB配置修改
DB_NAME = 'spider'
COLLECTION_NAME = '实习生'


def init_mongo():
    """初始化MongoDB连接"""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return collection


def parse_custom_font(font_file):
    """解析自定义字体文件，返回字符映射关系"""
    ocr = ddddocr.DdddOcr(show_ad=False)
    font = TTFont(font_file)
    cmap = font.getBestCmap()
    char_map = {}

    for code, name in cmap.items():
        char = chr(code)
        img = Image.new('RGB', (200, 200), color='red')
        draw = ImageDraw.Draw(img)
        draw.text(
            xy=(50, 50),
            text=char,
            font=ImageFont.truetype(font_file, size=100)
        )
        recognized = ocr.classification(img)
        char_map[char] = recognized

    return char_map


def fetch_intern_jobs(font_mapping, keyword='python', city='全国', job_type='intern'):
    """爬取实习信息并处理字体反爬"""
    url = f'https://www.shixiseng.com/interns?keyword={keyword}&city={city}&type={job_type}'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }

    response = requests.get(url=url, headers=headers)
    html = etree.HTML(response.text)
    divs = html.xpath('//div[@searchtype="intern"]')

    jobs = []
    for div in divs:
        # 处理岗位名称
        job = div.xpath('.//a[@class="title ellipsis font"]/text()')[0]
        job = replace_custom_chars(job, font_mapping)

        # 处理薪资
        money = div.xpath('.//span[@class="day font"]/text()')[0]
        money = replace_custom_chars(money, font_mapping).replace('o', '0')

        # 公司名称
        title = div.xpath('.//a[@class="title ellipsis"]/text()')[0]

        jobs.append({
            '职位': job,
            '薪资': money,
            '公司': title,
            '搜索关键词': keyword,
            '城市': city
        })

    return jobs


def replace_custom_chars(text, char_map):
    """替换文本中的自定义字符"""
    for char, replacement in char_map.items():
        text = text.replace(char, replacement)
    return text


def save_to_mongo(collection, data):
    """将数据保存到MongoDB"""
    try:
        result = collection.insert_many(data)
        print(f"成功插入 {len(result.inserted_ids)} 条数据")
        return True
    except Exception as e:
        print(f"数据保存失败: {e}")
        return False


def main():
    # 初始化MongoDB连接
    collection = init_mongo()

    # 1. 解析字体
    font_mapping = parse_custom_font('sxs.woff')

    # 2. 爬取数据
    jobs = fetch_intern_jobs(font_mapping)

    # 3. 保存到MongoDB
    if jobs:
        save_to_mongo(collection, jobs)

    # 4. 打印结果
    for job in jobs:
        print(f"职位: {job['职位']}\n薪资: {job['薪资']}\n公司: {job['公司']}\n{'=' * 30}")


if __name__ == '__main__':
    main()
