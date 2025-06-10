"""

https://www.shixiseng.com/interns?page=1&type=intern&keyword=python&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend=



"""
urls = [
    'https://www.shixiseng.com/interns?keyword=python'
]
for i in range(2,4):
    base_url = f'https://www.shixiseng.com/interns?page={i}&type=intern&keyword=python&area=&months=&days=&degree=&official=&enterprise=&salary=-0&publishTime=&sortType=&city=%E5%85%A8%E5%9B%BD&internExtend='
    urls.append(base_url)
print(urls)


