# 需要导入的模块
import requests
from lxml import etree
from get_music_url import get_url
import time
import random
for page in range(1,51):
    # 请求地址
    url = f'https://5sing.kugou.com/yc/list?t=2&l=&s=&p={page}'

    # 请求头
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    # 发送请求
    response = requests.get(url=url,headers=headers)
    html = etree.HTML(response.text)
    # 定位所有的标签
    dl_list = html.xpath('//div[@class="lists"]/dl')
    # 遍历标签
    for dl in dl_list:
        # 提取歌曲的名字
        name = dl.xpath('./dd/h3/a/text()')
        name = name[0] if name else ''
        # 提取歌曲id
        songid = dl.xpath('./dd[@class="l_action"]/a/@argid')
        songid = songid[0] if songid else ''
        # 获取歌曲的下载地址
        url = get_url(songid)
        print('歌曲的下载地址',url)
        time.sleep(random.uniform(0.5,1.5))
        # 发送请求
        res = requests.get(url)
        # 保存文件
        with open(f'./酷狗音乐/{name}.mp3','wb') as f:
            f.write(res.content)



