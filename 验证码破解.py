"""
1,滑动验证码的网站：https://www.geetest.com/adaptive-captcha

"""

# 1，进入到滑动验证的操作界面
from playwright.sync_api import sync_playwright
import re,random,ddddocr
import requests,time

def get_track(distance):
    """一个生成模拟人为拖动轨迹的算法"""
    track = []
    # 从哪个位置开始滑动
    current = 0
    # 减速的阈值
    mid = distance * 4 / 5
    # 时间
    t = 0.2
    # 速度
    v = 0
    while current < distance:
        if current < mid:
            a = 2  # 加速值
        else:
            a = -3
        v0 = v
        v = v0 + a * t  # 新的移动速度
        move = v0 * t + 1 / 2 * a * t * t  # 移动的距离
        track.append(round(move))  # 加入移动轨迹
        current += move  # current 记录当前位置
    track.append(distance - sum(track))
    return track

with sync_playwright() as pw:
    # 打开浏览器（设置浏览器全屏最大化）
    browser = pw.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.geetest.com/adaptive-captcha' ,wait_until='load')
    page.reload()
    time.sleep(2)
    # 定位选择的验证方式
    page.locator('//div[@class="tab-item tab-item-1"]').click()
    # 点击按钮开始验证
    page.locator('//div[@aria-label="点击按钮开始验证"]').click()
    page.wait_for_timeout(1000)
    # # 定位登入按钮
    # page.locator('//div[@class="login"]').click()
    # page.wait_for_timeout(2000)
    # 获取滑块图片的属性
    while True:
        slide = page.locator('.geetest_slice_bg').get_attribute('style')
        slide_url = re.search(r'url\("(.+?)"\)', slide).group(1)
        print("滑块图片的地址",slide_url)
        # 获取背景图的属性
        background = page.locator('.geetest_bg').get_attribute('style')
        background_url = re.search(r'url\("(.+?)"\)', background).group(1)
        print("背景图片的地址", background_url)
        # 下载图片和背景图
        slide_content = requests.get(slide_url).content
        background_content = requests.get(background_url).content
        # 识别滑动的轨迹宽度
        ocr = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        result = ocr.slide_match(slide_content, background_content, simple_target=True)
        print("识别结果", result)
        # 获取要滑动的距离(由于拖动的时候是通过滑块中间点去进行移动的，所以需要加上滑块按钮宽度的一半)
        # 1，定位滑块按钮元素,获取滑块按钮的宽度
        w = page.locator('.geetest_slice_bg').bounding_box()['width']
        x = result['target'][0] + w/2
        print("要滑动的距离为：", x)
        # 2,根据滑动的距离，生成滑动的轨迹
        dis = get_track(x)
        print("生成滑动的轨迹为：" , dis)
        # 3,进行滑动验证
        # 3.1 定位滑动按钮元素
        button = page.locator('div .geetest_btn')
        # 鼠标移动到元素上方
        button.hover()
        # 获取按钮的x,y坐标
        axis = button.bounding_box()
        x = axis['x']
        y = axis['y']
        # 3.2按下鼠标，不是点击
        page.mouse.down()
        # 鼠标移动的起始位置
        s_x = x
        s_y = y + random.randint(-5,5)
        # 拖动鼠标
        for i in dis:
            s_x += i
            page.mouse.move(s_x,s_y)
        # 确定鼠标拖动的最终距离
        page.mouse.move(s_x + random.randint(-5, 5), s_y)
        # 松开鼠标
        page.mouse.up()
        if page.locator("//div[text()='验证通过']").is_visible():
            break


        page.wait_for_timeout(4000)










