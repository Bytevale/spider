# 导入自动化模块
from DrissionPage import ChromiumPage
import time  # 将time模块导入移到顶部
import random
# 打开浏览器
dp = ChromiumPage()
# 先监听数据包
dp.listen.start('json/fetchHotelList')
# 访问网站
dp.get('https://hotels.ctrip.com/hotels/list?countryId=1&city=477&optionId=477&optionType=City&display=%E6%AD%A6%E6%B1%89')
# for循环下滑页面
for page in range(1,11):
    print(f'正在爬取第{page}页数据')
    
    if page > 2:
        next_page = dp.ele('css:.btn-box span')
        if next_page.text == '搜索更多酒店':
            # 点击搜索更多酒店
            next_page.click()
            time.sleep(3)  # 点击搜索更多后等待3秒让内容加载
    
    # 等待数据包加载
    resp = dp.listen.wait()
    
    # 获取响应数据内容
    json_data = resp.response.body
    
    # 提取并打印酒店名称和地址
    for hotel in json_data['data']['hotelList']:
        name = hotel['hotelInfo']['nameInfo']['name']
        address = hotel['hotelInfo']['positionInfo']['address']
        print(f"酒店名称: {name}, 地址: {address}")

    dp.scroll.to_bottom()
    time.sleep(random.uniform(2, 3))  # 随机等待2-3秒模拟真人操作
