import requests
# 1,准备请求地址
url = 'https://www.xfz.cn/api/website/articles/?p=2&n=20&type='
# 2，发送请求
response = requests.get(url=url)
# 3，获取返回的json数据，将json数据转化为对应的python数据格式
result = response.json()
# 4,通过字典和列表提取数据
data_list = result['data']
# print(data_list)
# 通过for循环对列表进行遍历
for item in data_list:
    print(item)




