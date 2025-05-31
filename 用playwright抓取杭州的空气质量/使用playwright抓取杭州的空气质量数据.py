from playwright.sync_api import sync_playwright
import pymongo

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page(ignore_https_errors=True)
    page.goto('https://www.aqistudy.cn/html/city_realtime.php?v=2.3',wait_until='load')
    # =========添加初始化js脚本代码，隐藏webdriver属性，防止检测出来(重点，以后写代码的时候，直接先加上这两行代码，确保万无一失)=====================
    js = "Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"
    page.add_init_script(js)
    page.wait_for_timeout(3000)
    datas = page.locator('//div[@class="datagrid-view2"]//div[@class="datagrid-body"]//tr').all()
    # print(datas)
    for item in datas:
        name = item.locator('//td[@field="pointname"]//span').inner_text()
        aqi = item.locator('//td[@field="aqi"]/div').inner_text()
        quality = item.locator('//td[@field="quality"]/div').inner_text()
        pm2_5 = item.locator('//td[@field="pm2_5"]/div').inner_text()
        print(name,aqi,quality,pm2_5)
