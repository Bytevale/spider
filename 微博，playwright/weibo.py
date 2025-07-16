# ... existing code ...import time
import random
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin


def crawl_weibo_accounts(keyword, max_pages=50):
    """
    爬取微博中带有特定关键词的账号

    参数:
        keyword: 搜索关键词(如"科龙空调")
        max_pages: 最大爬取页数
    """
    base_url = "https://s.weibo.com"
    results = []

    with sync_playwright() as p:
        # 启动浏览器(使用Chromium)
        browser = p.chromium.launch(headless=False)  # 设置为True可无头运行
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        try:
            for current_page in range(1, max_pages + 1):
                search_url = f"https://s.weibo.com/user?q={keyword}&Refer=weibo_user&page={current_page}"
                print(f"正在处理第 {current_page} 页...")

                # 打开当前页
                page.goto(search_url, timeout=60000)

                # 随机延迟模拟人工操作
                delay = random.uniform(5, 10)
                print(f"随机等待 {delay:.2f} 秒...")
                time.sleep(delay)

                # 等待账号信息加载完成
                try:
                    page.wait_for_selector('//div[@class="info"]/div/a', timeout=30000)
                except Exception:
                    print("页面加载超时或没有找到账号列表，请检查是否被跳转到验证码页")
                    with open(f"debug_page_{current_page}.html", "w", encoding="utf-8") as f:
                        f.write(page.content())
                    page.screenshot(path=f"error_screenshot_page_{current_page}.png")
                    continue

                # 提取账号名称和URL
                account_elements = page.query_selector_all('//div[@class="info"]/div/a')
                for element in account_elements:
                    account_name = element.inner_text().strip()
                    account_url = element.get_attribute('href')

                    if account_url:
                        full_url = urljoin(base_url, account_url)
                        results.append({
                            "account_name": account_name,
                            "account_url": full_url
                        })

                print(f"第 {current_page} 页找到 {len(account_elements)} 个账号")

        except Exception as e:
            print(f"爬取过程中出错: {str(e)}")
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            page.screenshot(path="error_screenshot.png")
        finally:
            # 关闭浏览器
            browser.close()

    return results


if __name__ == "__main__":
    keyword = "科龙空调"
    accounts = crawl_weibo_accounts(keyword, max_pages=50)

    print("\n爬取结果:")
    for i, account in enumerate(accounts, 1):
        print(f"{i}. 账号名称: {account['account_name']}")
        print(f"   账号URL: {account['account_url']}\n")

    with open("weibo_accounts.txt", "w", encoding="utf-8") as f:
        for account in accounts:
            f.write(f"{account['account_name']}\t{account['account_url']}\n")

    print(f"共找到 {len(accounts)} 个账号，结果已保存到 weibo_accounts.txt")
