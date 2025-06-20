from playwright.sync_api import sync_playwright
import time
import random
from openpyxl import Workbook

# 你的登录信息 - 请替换为实际值
PHONE_NUMBER = "你的手机号"
PASSWORD = "你的密码"

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    js = "Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"
    page.add_init_script(js)

    # 创建一个Excel工作簿
    wb = Workbook()
    ws = wb.active
    ws.title = "政策数据"

    # 写入表头
    ws.append(["标题", "内容", "发布机构", "领域", "发布日期"])

    # 初始页面
    url = 'https://www.spolicy.com/search?keyword=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD'
    page.goto(url)
    time.sleep(random.uniform(2, 4))

    # 先点击"加载更多"按钮
    try:
        load_more = page.locator('//*[@id="app"]/div/div/main/div[3]/div[1]/button/span[2]/span')
        load_more.scroll_into_view_if_needed()
        load_more.click()
        time.sleep(random.uniform(2, 3))
        print("已点击'加载更多'按钮")
    except Exception as e:
        print(f"点击'加载更多'按钮失败: {e}")

    logged_in = False  # 登录状态标志

    # 翻页10次
    for page_num in range(10):
        print(f"正在爬取第 {page_num + 1} 页...")

        # 等待元素加载完成
        page.wait_for_selector('//div[@class="py-5"]', timeout=30000)

        div_list = page.locator('//div[@class="py-5"]').all()
        for item in div_list:
            try:
                # 获取数据项
                title_locator = item.locator('//a[@class="policy-item mb-5 block"]/div[1]')
                title_locator.wait_for(timeout=10000)
                title = title_locator.inner_text()

                content_locator = item.locator('//a[@class="policy-item mb-5 block"]/div[2]')
                content_locator.wait_for(timeout=10000)
                content = content_locator.inner_text()

                institute_locator = item.locator('//span[@class="mr-4"]')
                institute_locator.wait_for(timeout=10000)
                institute = institute_locator.inner_text()

                domain_locator = item.locator('//div[contains(@class, "text-xs")]/span[2]')
                domain_locator.wait_for(timeout=10000)
                domain = domain_locator.inner_text()

                date_locator = item.locator('//div[contains(@class, "text-xs")]/span[3]')
                date_locator.wait_for(timeout=10000)
                date = date_locator.inner_text()

                # 将数据写入Excel
                ws.append([title, content, institute, domain, date])
                print(f"已收集：{title}")

            except Exception as e:
                print(f"获取数据失败: {e}")
                continue

        # 点击"下一页"按钮
        try:
            next_page = page.locator('//button[@aria-label="下一页"]')
            next_page.wait_for(timeout=30000)
            next_page.scroll_into_view_if_needed()
            next_page.click()
            time.sleep(random.uniform(3, 5))
            print("已点击'下一页'按钮")

            # 第一次点击下一页后检查是否需要登录
            if not logged_in and page_num == 0:
                try:
                    # 检查登录弹窗是否出现
                    phone_input = page.locator('//input[@aria-label="请输入登录手机号"]')
                    phone_input.wait_for(timeout=5000)

                    # 填写登录信息
                    phone_input.fill(PHONE_NUMBER)
                    time.sleep(random.uniform(1, 2))

                    password_input = page.locator('//input[@aria-label="请输入登录密码"]')
                    password_input.fill(PASSWORD)
                    time.sleep(random.uniform(1, 2))

                    # 点击登录按钮 (假设有登录按钮)
                    login_button = page.locator('//button[contains(text(),"登录")]')
                    login_button.click()
                    time.sleep(random.uniform(3, 5))

                    logged_in = True
                    print("已填写登录信息并提交")
                except Exception as e:
                    print(f"未检测到登录弹窗或登录失败: {e}")

        except Exception as e:
            print(f"点击'下一页'按钮失败: {e}")
            break

    # 保存Excel文件
    wb.save("policy.xlsx")
    print("数据已保存到 policy.xlsx 文件")
    browser.close()
