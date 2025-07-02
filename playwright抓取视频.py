import requests
import random
import time
from playwright.sync_api import sync_playwright
import tempfile

# 监听响应下载视频的函数
def deal_video(response):
    # 1.筛选返回内容是视频的请求
    status = response.status
    content = response.headers.get('content-type')
    if status == 206 and content == 'video/mp4':
        video_url = response.url
        print(f"视频请求地址：{video_url}")

        # 2.下载保存视频
        request_response = requests.get(url=video_url, headers=response.request.headers)
        filename = "./spider/video/" + video_url.split('?')[0][-20:]
        with open(filename, 'wb') as f:
            f.write(request_response.content)


# 步骤二：playwright连接谷歌
with sync_playwright() as p:
    # 使用系统临时目录作为用户数据目录
    user_data_dir = tempfile.mkdtemp()

    broswer = p.chromium.launch_persistent_context(
        # 1.指定本地谷歌安装目录的绝对路径
        executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        # 2.使用临时目录代替受保护的系统目录
        user_data_dir=user_data_dir,

        # 3.开启有界面模式
        headless=False
    )

    # 2.创建页面
    page = broswer.new_page()

    # 删除了对 stealth.min.js 的引用，避免文件未找到错误

    page.on('response', deal_video)  # 部署一个响应监听器，用来获取视频内容对应的请求信息

    # 访问网站
    page.goto('https://www.kuaishou.com/profile/3xg2qk7h98uu7pe')
    page.wait_for_timeout(2000)
    page.reload()  # 刷新页面
    page.wait_for_timeout(2000)

    # 获取作品总数
    number = page.locator('//div[@class="user-detail-item"]/h3').inner_text()
    print(f"该博主共有{number}个作品", type(number))  # 作品总数以字符串形式返回

    # 定位第一个视频
    first_video = page.locator('//div[@class="video-card-main"]').first

    # 点击第一个视频，进入到刷视频页面
    first_video.click()

    # 循环刷视频
    for i in range(int(number)-1):
        # 模拟人观看视频的操作，每个视频随机停留1~7秒
        page.wait_for_timeout(random.randint(1000, 7000))
        # 点击播放下一个视频
        next_button = page.locator('//div[@class="switch-item video-switch-next"]')
        next_button.click()

    page.wait_for_timeout(2000)
