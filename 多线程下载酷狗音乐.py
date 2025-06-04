import requests,time
from lxml import etree

import execjs
from threading import Thread

# ================第一步：生成50个网页=======================
url_list = []
for i in range(1,51):
    url = f'https://5sing.kugou.com/yc/list?t=2&l=&s=&p={i}'
    url_list.append(url)
# ================第二页：把50个网页拆分成10个任务去执行=============
def get_url(songid):
    # 生成时间戳
    t = int(time.time() * 1000)
    # 需要调整顺序和浏览器请求发送的一样
    # n.join("")，在console运行后可以看到
    """
    # 5uytoxQewcvIc1gn1PlNF0T2jbbOzRl5
    # appid=2918
    # clienttime=1748438129174
    # clientver=1000
    # dfid=3x6ya42vfm0Q4RYHXr3Hok8R
    # mid=219923f078143dc75af476e99a3190b7
    # songid=4343319
    # songtype=yc
    # uuid=219923f078143dc75af476e99a3190b7
    # version=6.6.72
    # 5uytoxQewcvIc1gn1PlNF0T2jbbOzRl5
    """
    # 准备请求参数（核心）
    params = {
        'appid': "2918",
        "clienttime": t,
        'clientver': "1000",
        'dfid': "3x6ya42vfm0Q4RYHXr3Hok8R",
        'mid': "219923f078143dc75af476e99a3190b7",
        "songid": songid,
        'songtype': 'yc',
        'uuid': "219923f078143dc75af476e99a3190b7",
        "version": "6.6.72",
    }
    # 将字典格式的参数转化为加密时所需的列表格式，然后在拼接为字符串
    li = []
    li.append("5uytoxQewcvIc1gn1PlNF0T2jbbOzRl5")
    for k, v in params.items():
        li.append(f'{k}={v}')
    li.append("5uytoxQewcvIc1gn1PlNF0T2jbbOzRl5")
    # 获取加密是所需的最终参数
    ss = ''.join(li)
    # ===========调用js中的代码进行加密，生成最终的密文==============
    js_code = """function p(e, t, n, o, r, i, a) {
                return l(n ^ (t | ~o), e, t, r, i, a)
            }
    function g(e, t, n, o, r, i, a) {
                return l(t ^ n ^ o, e, t, r, i, a)
            }
    function f(e, t, n, o, r, i, a) {
                return l(t & o | n & ~o, e, t, r, i, a)
            }
    function u(e, t) {
                var n = (65535 & e) + (65535 & t);
                return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
            }
    function l(e, t, n, o, r, i) {
                return u((i = u(u(t, e), u(o, i))) << r | i >>> 32 - r, n)
            }
    function m(e, t, n, o, r, i, a) {
                return l(t & n | ~t & o, e, t, r, i, a)
            }
    function n(e) {
        return unescape(encodeURIComponent(e))
    }
    function s(e) {
                var t = [];
                for (t[(e.length >> 2) - 1] = void 0,
                o = 0; o < t.length; o += 1)
                    t[o] = 0;
                for (var n = 8 * e.length, o = 0; o < n; o += 8)
                    t[o >> 5] |= (255 & e.charCodeAt(o / 8)) << o % 32;
                return t
            }
    function a(e, t) {
                var n, o, r, i;
                e[t >> 5] |= 128 << t % 32,
                e[14 + (t + 64 >>> 9 << 4)] = t;
                for (var a = 1732584193, l = -271733879, c = -1732584194, s = 271733878, d = 0; d < e.length; d += 16)
                    a = m(n = a, o = l, r = c, i = s, e[d], 7, -680876936),
                    s = m(s, a, l, c, e[d + 1], 12, -389564586),
                    c = m(c, s, a, l, e[d + 2], 17, 606105819),
                    l = m(l, c, s, a, e[d + 3], 22, -1044525330),
                    a = m(a, l, c, s, e[d + 4], 7, -176418897),
                    s = m(s, a, l, c, e[d + 5], 12, 1200080426),
                    c = m(c, s, a, l, e[d + 6], 17, -1473231341),
                    l = m(l, c, s, a, e[d + 7], 22, -45705983),
                    a = m(a, l, c, s, e[d + 8], 7, 1770035416),
                    s = m(s, a, l, c, e[d + 9], 12, -1958414417),
                    c = m(c, s, a, l, e[d + 10], 17, -42063),
                    l = m(l, c, s, a, e[d + 11], 22, -1990404162),
                    a = m(a, l, c, s, e[d + 12], 7, 1804603682),
                    s = m(s, a, l, c, e[d + 13], 12, -40341101),
                    c = m(c, s, a, l, e[d + 14], 17, -1502002290),
                    a = f(a, l = m(l, c, s, a, e[d + 15], 22, 1236535329), c, s, e[d + 1], 5, -165796510),
                    s = f(s, a, l, c, e[d + 6], 9, -1069501632),
                    c = f(c, s, a, l, e[d + 11], 14, 643717713),
                    l = f(l, c, s, a, e[d], 20, -373897302),
                    a = f(a, l, c, s, e[d + 5], 5, -701558691),
                    s = f(s, a, l, c, e[d + 10], 9, 38016083),
                    c = f(c, s, a, l, e[d + 15], 14, -660478335),
                    l = f(l, c, s, a, e[d + 4], 20, -405537848),
                    a = f(a, l, c, s, e[d + 9], 5, 568446438),
                    s = f(s, a, l, c, e[d + 14], 9, -1019803690),
                    c = f(c, s, a, l, e[d + 3], 14, -187363961),
                    l = f(l, c, s, a, e[d + 8], 20, 1163531501),
                    a = f(a, l, c, s, e[d + 13], 5, -1444681467),
                    s = f(s, a, l, c, e[d + 2], 9, -51403784),
                    c = f(c, s, a, l, e[d + 7], 14, 1735328473),
                    a = g(a, l = f(l, c, s, a, e[d + 12], 20, -1926607734), c, s, e[d + 5], 4, -378558),
                    s = g(s, a, l, c, e[d + 8], 11, -2022574463),
                    c = g(c, s, a, l, e[d + 11], 16, 1839030562),
                    l = g(l, c, s, a, e[d + 14], 23, -35309556),
                    a = g(a, l, c, s, e[d + 1], 4, -1530992060),
                    s = g(s, a, l, c, e[d + 4], 11, 1272893353),
                    c = g(c, s, a, l, e[d + 7], 16, -155497632),
                    l = g(l, c, s, a, e[d + 10], 23, -1094730640),
                    a = g(a, l, c, s, e[d + 13], 4, 681279174),
                    s = g(s, a, l, c, e[d], 11, -358537222),
                    c = g(c, s, a, l, e[d + 3], 16, -722521979),
                    l = g(l, c, s, a, e[d + 6], 23, 76029189),
                    a = g(a, l, c, s, e[d + 9], 4, -640364487),
                    s = g(s, a, l, c, e[d + 12], 11, -421815835),
                    c = g(c, s, a, l, e[d + 15], 16, 530742520),
                    a = p(a, l = g(l, c, s, a, e[d + 2], 23, -995338651), c, s, e[d], 6, -198630844),
                    s = p(s, a, l, c, e[d + 7], 10, 1126891415),
                    c = p(c, s, a, l, e[d + 14], 15, -1416354905),
                    l = p(l, c, s, a, e[d + 5], 21, -57434055),
                    a = p(a, l, c, s, e[d + 12], 6, 1700485571),
                    s = p(s, a, l, c, e[d + 3], 10, -1894986606),
                    c = p(c, s, a, l, e[d + 10], 15, -1051523),
                    l = p(l, c, s, a, e[d + 1], 21, -2054922799),
                    a = p(a, l, c, s, e[d + 8], 6, 1873313359),
                    s = p(s, a, l, c, e[d + 15], 10, -30611744),
                    c = p(c, s, a, l, e[d + 6], 15, -1560198380),
                    l = p(l, c, s, a, e[d + 13], 21, 1309151649),
                    a = p(a, l, c, s, e[d + 4], 6, -145523070),
                    s = p(s, a, l, c, e[d + 11], 10, -1120210379),
                    c = p(c, s, a, l, e[d + 2], 15, 718787259),
                    l = p(l, c, s, a, e[d + 9], 21, -343485551),
                    a = u(a, n),
                    l = u(l, o),
                    c = u(c, r),
                    s = u(s, i);
                return [a, l, c, s]
            }
    function c(e) {
        for (var t = "", n = 32 * e.length, o = 0; o < n; o += 8)
            t += String.fromCharCode(e[o >> 5] >>> o % 32 & 255);
        return t
    }
    function r(e) {
        return c(a(s(e = n(e)), 8 * e.length))
    }
    function o(e) {
            for (var t, n = "0123456789abcdef", o = "", r = 0; r < e.length; r += 1)
                t = e.charCodeAt(r),
                o += n.charAt(t >>> 4 & 15) + n.charAt(15 & t);
            return o
        }
    function t(e, t, n) {
                return t ? n ? i(t, e) : o(i(t, e)) : n ? r(e) : o(r(e))
            }

    """
    # 编译js代码
    js = execjs.compile(js_code)
    result = js.call('t', ss)
    params['signature'] = result
    # print("加密得到的参数" , result)
    # ================发送请求获取歌曲下载地址==========
    url = 'https://5sservice.kugou.com/song/getsongurl'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "cookie": "kg_mid=219923f078143dc75af476e99a3190b7; kg_dfid=3x6ya42vfm0Q4RYHXr3Hok8R; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_mid_temp=219923f078143dc75af476e99a3190b7; cct=63801eba; 5SING_TAG_20250528=GF_ST-19.STW-0.SC-0.PL-0.FX-0.ZF-0.ZC-0.XZ-0.DZ-0%7CLX_ST-19.STW-0.SC-0.PL-0.FX-0.ZF-0.ZC-0.XZ-0.DZ-0%7CHY_ST-19.STW-0.SC-0.PL-0.FX-0.ZF-0.ZC-0.XZ-0.DZ-0",
        "referer": "https://5sing.kugou.com/"
    }
    # 发送请求
    res = requests.get(url=url, params=params, headers=headers)
    res = res.json()
    music_url = res['data']['lqurl']
    return music_url
def work(urls):
    for page_url in urls:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        # 发送请求
        response = requests.get(url=page_url, headers=headers)

        # ==================通过xpath提取歌曲的id====================
        html = etree.HTML(response.text)
        # 定位包含所有的歌曲的标签
        dl_list = html.xpath('//div[@class="lists"]/dl')
        # 对定位到的dl标签进行遍历，挨个提取歌曲的名称和ID
        for dl in dl_list:
            # 提取歌曲名字
            name = dl.xpath('.//dd[@class="l_info"]/h3/a/text()')
            name = name[0] if name else ''
            # 提取歌曲的id
            music_id = dl.xpath('.//a[@class="m_date_shou"]/@argid')
            music_id = music_id[0] if music_id else ''
            print({"名字": name, "id": music_id})
            # 获取歌曲的下载地址
            url = get_url(music_id)
            print("下载地址：", url)
            resp = requests.get(url)
            # # 保存为文件
            with open(f'music/{name}.mp3', 'wb') as f:
                f.write(resp.content)
# 10个人采集
Thread(target=work, kwargs={"urls":url_list[0:5]}).start()
Thread(target=work, kwargs={"urls":url_list[5:10]}).start()
Thread(target=work, kwargs={"urls":url_list[10:15]}).start()
Thread(target=work, kwargs={"urls":url_list[15:20]}).start()
Thread(target=work, kwargs={"urls":url_list[20:25]}).start()
Thread(target=work, kwargs={"urls":url_list[25:30]}).start()
Thread(target=work, kwargs={"urls":url_list[30:35]}).start()
Thread(target=work, kwargs={"urls":url_list[35:40]}).start()
Thread(target=work, kwargs={"urls":url_list[40:45]}).start()
Thread(target=work, kwargs={"urls":url_list[45:50]}).start()
