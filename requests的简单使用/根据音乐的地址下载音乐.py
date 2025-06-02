import requests

# 1,准备请求的地址
url = 'https://m704.music.126.net/20250602200901/48ff797a9609b910c6e28ea3674e30b9/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/60186688244/1c92/4134/4e96/28e34d5bace566eaa36617bbcfc3ceff.m4a?vuutv=4yT7OiVBZ9Sg9IpB/DNTgR8RAcZcfNF6U5htpJZZgm3JqAlVWDc0sPeYUkGFy46adfdHgPIWgC1DMdOaO2dMcqKmKt3sgo3IXJ2/iaoDYbs=&authSecret=000001973074a9e816a70a3b18b508fe'
# 2,发送请求
response = requests.get(url = url)
# 3,获取请求内容
result = response.content
# 4，将抓取的数据保存文件
# 4.1，打开文件
with open('music/土像女孩.m4a','wb') as file:
    # 4.2,写入文件
    file.write(result)

