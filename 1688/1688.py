import requests
from lxml import etree
from openpyxl import load_workbook  # 修改这里
import time
import random
import json
from DrissionPage import ChromiumPage
import re

# 加载已存在的 Excel 工作簿
wb = load_workbook('data.xlsx')
ws = wb.active  # 或者使用 wb['SheetName'] 来选择特定的工作表

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}

# 创建浏览器页面对象
page = ChromiumPage()

for page_num in range(1, 51):
    for num in range(1, 7):
        url = f'https://p4psearch.1688.com/hamlet/async/v1.json?beginpage={page_num}&asyncreq={num}&keywords=&keyword=%E5%8D%AB%E6%B5%B4%E3%80%81&sortType=&descendOrder=&province=&city=&priceStart=&priceEnd=&dis=&ptid=&exp=pcSemFumian%3AC%3BpcDacuIconExp%3AA%3BpcCpxGuessExp%3AB%3BcplLeadsExp%3AA%3BpcCpxCpsExp%3AB%3Bqztf%3AE%3BdownloadIconExp%3AC%3BhotBangdanExp%3AB%3BpcSemWwClick%3AA%3Basst%3AE&cosite=&salt=17519556352735&sign=1374d274a94586ea54a12ae5ce616570&hmaTid=3&hmaQuery=graphDataQuery&pidClass=pc_list_336&cpx=cpc%2Cfree%2Cnature&api=pcSearch&pv_id='
        response = requests.get(url=url, headers=headers)
        json_data = response.json()
        lis = json_data['module']['offer']['list']
        for li in lis:
            # 获取商品详情页链接
            odUrl = li.get('odUrl')
            shop_score = ''

            if odUrl:
                time.sleep(random.uniform(3, 5))

                try:
                    page.get(odUrl)
                    page.wait(4) # 等待页面加载

                    # 尝试多种定位方式获取评分
                    score_text = ''
                    ele = page.ele('xpath://span[@class="v-flex"]/em', timeout=3) or \
                          page.ele('xpath://span[contains(@class,"score")]', timeout=2) or \
                          page.ele('xpath://*[contains(text(),"分")]', timeout=2)

                    if ele:
                        score_text = ele.text
                        # 使用正则提取评分数字
                        shop_score = re.search(r'\d+\.\d+', score_text).group() if score_text else ''
                    else:
                        shop_score = ''
                except Exception as e:
                    print(f"获取评分失败: {e}")
                    shop_score = ''

            row_data = [
                li['subject'],
                li['price'],
                li['saleVolume'],
                li['loginId'],
                shop_score,
                li['imgUrl']
            ]
            ws.append(row_data)
            print(row_data)
            wb.save('data.xlsx')  # 每次只保存当前行

# 关闭浏览器
page.quit()
