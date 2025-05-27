from DrissionPage import ChromiumPage , ChromiumOptions # 自动化模块
from DrissionPage.common import Actions # 导入动作链
from DrissionPage.common import Keys # 导入键盘
from pypinyin import pinyin, Style
import json
import requests

def language(chinese):
    zw = pinyin(chinese,style=Style.NORMAL)
    string = ''.join([t[0] for t in zw])
    return string
def buy(Go_city,To_city,Sj,page_num):
    co = ChromiumOptions().set_browser_path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")  # 修改为你的实际路径
    zdh = ChromiumPage(addr_or_opts=co)
    # 自动打开浏览器
    # zdh = ChromiumPage()
    dzl = Actions(zdh)
    # 自动打开网页地址
    zdh.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%93%88%E5%B0%94%E6%BB%A8%E5%8C%97,HTB&ts=%E5%B9%BF%E5%B7%9E%E5%8C%97,GBQ&date=2025-05-31&flag=N,N,Y')
    # 元素定位
    dzl.move_to('css:#fromStationText').click().type(language(Go_city)) # 定位出发地输入框元素
    zdh.ele('css:#fromStationText').input(Keys.ENTER) # 输入回车

    dzl.move_to('css:#toStationText').click().type(language(To_city)) # 定位目的地输入框元素
    zdh.ele('css:#toStationText').input(Keys.ENTER) # 输入回车

    zdh.ele('css:#train_date').clear() # 清楚原有时间
    zdh.ele('css:#train_date').input(Sj) # 定位出发时间的输入框

    zdh.ele('css:#query_ticket').click("") # 定位查询按钮

    zdh.ele(f'css:#queryLeftTable tr:nth-child({int(page_num)*2-1}) .btn72').click("") # 定位预定车票的位置

    zdh.ele('css:#J-userName').input("") # 请输入电话号码
    zdh.ele('css:#J-password').input("") # 请输入密码
    zdh.ele('css:#J-login').click() # 登入元素定位
    zdh.ele('css:#id_card').input(8597) # 请输入身份证后四位
    zdh.ele('css:#verification_code').click() # 点击发送验证码
    yzm = int(input("请输入您的验证码："))
    zdh.ele('css:#code').input(yzm) # 请输入验证码
    zdh.ele('css:#sureClick').click() # 确定登入


# 导入城市代码json文件
k = open('city.json',encoding='utf-8').read()
city = json.loads(k)

go_city = input("请输入您的出发城市：")
to_city = input("请输入您的目标城市：")
sj = input("请输入出发时间：")


# url = f'https://kyfw.12306.cn/otn/leftTicket/queryG?leftTicketDTO.train_date={sj}&leftTicketDTO.from_station={city[go_city]}&leftTicketDTO.to_station={city[to_city]}&purpose_codes=ADULT'
url = f'https://kyfw.12306.cn/otn/leftTicket/queryU?leftTicketDTO.train_date={sj}&leftTicketDTO.from_station={city[go_city]}&leftTicketDTO.to_station={city[to_city]}&purpose_codes=ADULT'
headers = {
    "referer":"https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%93%88%E5%B0%94%E6%BB%A8,HBB&ts=%E5%B9%BF%E5%B7%9E,GZQ&date=2025-05-31&flag=N,N,Y",
    "cookie":"_uab_collina=174695067925664656979961; JSESSIONID=2BC549ECBBF1B9D754481B411985EC04; tk=H_QHjWgmbP7ApDpukwO6ePxKv0CeBm257B7_IiAl5wIhug1g0; _jc_save_fromStation=%u54C8%u5C14%u6EE8%2CHBB; _jc_save_toStation=%u5E7F%u5DDE%2CGZQ; _jc_save_wfdc_flag=dc; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1591279882.64545.0000; BIGipServerpassport=803733770.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_fromDate=2025-05-31; _jc_save_toDate=2025-05-26; uKey=60cdbec4ffc20c43a92fd04829f14cd1754e9e0d3a3a1930446a52c4a438c782",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

response = requests.get(url=url,headers=headers)

jsons = response.json()
# print(jsons)
data = jsons['data']['result']
# print(data)
page_num = 0
for i in data:
    index = i.split('|')
    page_num+=1
    trips = index[3] # 车次
    go_time = index[8] # 出发时间
    to_time = index[9] # 到达时间
    time = index[10] # 用时
    first_sleeper = index[23] # 一等卧
    second_sleeper = index[28] # 二等卧
    hardSeat = index[29] # 硬座

    dit = {
        '序号':page_num,
        '车次': trips,
        '出发时间': go_time,
        '到达时间': to_time,
        '用时': time,
        '一等卧': first_sleeper,
        '二等卧':second_sleeper,
        '硬座':hardSeat
    }
    print(dit)
page_num = input("请输入对应的车次序号：")
buy(Go_city=go_city,To_city=to_city,Sj=sj,page_num=page_num)
#
#
#




















