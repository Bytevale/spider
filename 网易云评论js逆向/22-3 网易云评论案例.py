"""
1.目标：采集网易云一首歌曲的评论数据   https://music.163.com/#/song?id=2603423529
2.流程：
    -1.数据位置：一级目录
    -2.数据类型：json
    -3.请求方法：post
       查看请求的data参数


js逆向笔记
1.js逆向主要找js文件  css html > pass
2.刷新可以实现js断点 但是如果js加密是通过判断网页缓存来执行的，最好点下一页
3.调试不同页数的参数发现 没有发生变化的参数值就直接在js文件里面写固定 如果说会发生变化的，后期要随着请求的页数变化而变化
4.JSON.stringify() 把字典 >> 字符串的方法
5.!function() {}();  自执行函数 不需要进行调用，可以自动运行的(需要运行文件！)
6.ReferenceError: window is not defined
    最容易遇到的报错 xxx 没有被定义 ！！
    解决 需要手动定义！！
    window=global;      window={};        window=this;
7.缺啥补啥！！

8.全局搜索关键时 可以加 空格 或者 等号 搜索

9.发现定义的位置在调用的位置上面 而且在同一个文件，从定义的位置 一直复制到调用到位置 先调试第一遍@
 如果定义的变量多了，不调用，没事的
"""
import requests
import json
import execjs
import jsonpath

with open('wyy.js','r',encoding="utf-8") as f:
    js_data = f.read()

exe = execjs.compile(js_data)


aaaa = {"rid":"R_SO_4_2603423529","threadId":"R_SO_4_2603423529","pageNo":"9","pageSize":"20","cursor":"1741063636999","offset":"0","orderType":"1","csrf_token":""}
args1 = json.dumps(aaaa)
# 通过exe.call方法调用
result = exe.call('get',args1)

data = {
    'params':result['params'],
    'encSecKey':result['encSecKey']
}
# 请求评论的url
url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='

headers_ = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Referer':'https://music.163.com/song?id=2603423529'
}

response = requests.post(url,headers=headers_,data=data).json()

nickname = jsonpath.jsonpath(response,'$..nickname')
content = jsonpath.jsonpath(response,'$..content')

for i in zip(nickname,content):
    print(i)


# w0TatJzLmXqkP+pytJRKFc+Xn3Vs0tSlf2Gj1/PpPKBQZVZCYXfaO1N48urW2X4UdEgo5DrLEwzDpYayTTMO/zBR6nKfkV12P9nRuKpIoF+LXIkStWhPEg71kh92RSlqDBOK5j+EX9Zh++tPAN+KGSwIu6+X9L5rQex9WUCgPigrvB2RFgk9iUDucMs+FYHL7duyVdgvy+CRQVYiaJm1j9YQCNHEHYy6G6WHNeckAmGX+XqbXo2seaipwBEXaB06D7ImWloYY8y61MpZP7zhd05/uXygSwZGDm2UQyxTh9o=
# +1lFiMYs3vZ0XaUvAbpg5uF3FrTZeIGSVcWqM8tQffBlL934uXZcoD4Tt6npJj4jI+dBSNhRzvrw2ZR/0pwKy4B1BB24TsSBEvlch5DEWoTyc9gFK/BVPDeThFbG3ZqeqtOZeKEnte83NEE5VTFpBYaHW8aLcExM5yq/6lPnoRpt+pyKWvr7+xVv2xYfrOy+SYUFI6OdafFuAsWNOFuFah+tssa8s/W3uIeeRRc+ZnV5mjhQmJAfuk/wSmp9hVbqsRtosSdZL3nmFyxaSOLxKvfOBaVcgLpMc73/yynQ84g=
# 1317267dd490c0c9fd2b4e2da6d1a72fafbd801d8e09d2b5a778c8b084e163458aaf52942659c8cda934f3435ebc3b8889291c89be2f3a853f3ea6b49d1a5e3753be928785bec6d8978128cacf19c68a0808be26d103d6a9f1098caf2ae333d6767643de57a230a1fe700bb0d0f33702b86ec92841da4998eb9642edc377f748
# 056d196898d4e2a51a39cb86ebd1ba7f372d6192795df08577649dfed1ef9847025fd5c7d8326a7b726cc321af5fa288f35ef55385be968bb81e24b795ee155005fafd4d702030c2e63a6bdd1e0521b6979daf9019f3103868eaccde87a9ba34781831a02ebf545a036b683dc0a1b7fc2e6c88fea6f0c68d798d5ed33af70b76


# 第3页评论响应内容里面的     "cursor": "1727012499146"
# 请求第4页评论数据需要携带的 "cursor": "1727012499146"