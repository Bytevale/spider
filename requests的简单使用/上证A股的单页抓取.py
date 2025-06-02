import requests
import time

# 请求地址
url = 'https://56.push2.eastmoney.com/api/qt/clist/get'
# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
# 获取时间戳
t = int(time.time() * 1000)
# 请求参数
params = {
    "pn": 1,
    "pz": 20,
    "np": 1,
    "po": 1,
    # 上证A股的数据采集
    "fs": "m:1 t:2,m:1 t:23",
    "fid": "f3",
    "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
    "ut": "bd1d9ddb04089700cf9c27f6f7426281",
    '_': t,
    "fltt": 2,
    "invt": 2,
    "dect": 1,
    "wbp2u": "|0|0|0|web"
}
# 发送请求
response = requests.get(url=url,headers=headers,params=params)
# 获取请求内容
result = response.json()
# print(result)
# 获取当前页面所有的股票数据
lists = result['data']['diff']
# print(lists)
for item in lists:
    name = item['f14']
    code = item['f12']
    gains = item['f3']
    print(f'股票名称：{name},股票代码：{code},今日涨幅：{gains}')










