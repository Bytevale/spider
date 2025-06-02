import requests
# 1,准备要下载的图片地址
url = 'https://wx2.sinaimg.cn/mw690/711c9a7bly1hxv2p6flmpj20nv1hcdno.jpg'
# 2，发送请求
response = requests.get(url = url)
# 3,获取返回的响应内容
result = response.content
# 4,将返回的响应内容保存为文件
# 4.1,打开文件
with open('picture/cute_girl.jpg', 'wb') as file:
    # 4.2,写入内容
    file.write(result)









