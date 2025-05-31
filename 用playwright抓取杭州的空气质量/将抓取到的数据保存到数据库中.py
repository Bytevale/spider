from playwright.sync_api import sync_playwright
from pymongo import MongoClient
import datetime

# 连接MongoDB数据库
client = MongoClient('mongodb://localhost:27017/')  # 默认本地连接
db = client['spider']  # 使用spider数据库
collection = db['杭州空气质量']  # 自动创建集合

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page(ignore_https_errors=True)
    page.goto('https://www.aqistudy.cn/html/city_realtime.php?v=2.3', wait_until='load')

    # 隐藏webdriver属性
    js = "Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"
    page.add_init_script(js)
    page.wait_for_timeout(3000)

    # 抓取数据
    datas = page.locator('//div[@class="datagrid-view2"]//div[@class="datagrid-body"]//tr').all()
    for item in datas:
        # 提取数据
        data = {
            '监测点': item.locator('//td[@field="pointname"]//span').inner_text(),
            'AQI': item.locator('//td[@field="aqi"]/div').inner_text(),
            '质量等级': item.locator('//td[@field="quality"]/div').inner_text(),
            'PM2.5': item.locator('//td[@field="pm2_5"]/div').inner_text(),
            '抓取时间': datetime.datetime.now()  # 记录抓取时间
        }

        # 打印数据（可选）
        print(f"{data['监测点']} - AQI: {data['AQI']}")

        # 存入MongoDB
        collection.insert_one(data)

    browser.close()
    client.close()  # 关闭数据库连接

print("数据已成功保存到MongoDB!")
