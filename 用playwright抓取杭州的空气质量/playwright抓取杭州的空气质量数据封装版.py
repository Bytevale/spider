from playwright.sync_api import sync_playwright
from pymongo import MongoClient  # 导入MongoDB客户端


class AQIScraper:
    def __init__(self, headless=False):
        self.headless = headless
        # 连接MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')  # 默认本地连接
        self.db = self.client['spider']  # 使用spider数据库
        self.collection = self.db['杭州空气质量']  # 使用杭州空气质量集合

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()
        self.playwright.stop()
        self.client.close()  # 关闭MongoDB连接

    def scrape_hangzhou_aqi(self):
        """抓取杭州空气质量数据并存入MongoDB"""
        page = self.browser.new_page(ignore_https_errors=True)
        try:
            page.goto('https://www.aqistudy.cn/html/city_realtime.php?v=2.3', wait_until='load')
            js = "Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"
            page.add_init_script(js)
            page.wait_for_timeout(3000)

            datas = page.locator('//div[@class="datagrid-view2"]//div[@class="datagrid-body"]//tr').all()
            for item in datas:
                data = {
                    '监测点': item.locator('//td[@field="pointname"]//span').inner_text(),
                    'AQI': item.locator('//td[@field="aqi"]/div').inner_text(),
                    '质量等级': item.locator('//td[@field="quality"]/div').inner_text(),
                    'PM2.5': item.locator('//td[@field="pm2_5"]/div').inner_text(),
                    '抓取时间': datetime.datetime.now()  # 添加抓取时间戳
                }
                # 插入数据到MongoDB
                self.collection.insert_one(data)
                print(f"已插入数据: {data['监测点']}")
        finally:
            page.close()


# 使用示例
if __name__ == "__main__":
    import datetime  # 导入时间模块

    with AQIScraper(headless=False) as scraper:
        print("开始抓取杭州空气质量数据...")
        scraper.scrape_hangzhou_aqi()
        print("数据抓取并存储完成！")
