import requests
import execjs
import time
url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token=d497be3121e96997ef8bdba8faf56edb'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'referer': 'https://music.163.com/song?id=190449',
    'cookie': '_ga=GA1.1.1818727316.1746165943; NMTID=00OqPScb8XpdX3zf0vsmMfmOCUT2mYAAAGWj5nKog; _ga_Z0JVTF6WF2=GS1.1.1746165943.1.0.1746165945.0.0.0; _iuqxldmzr_=32; _ntes_nnid=641e91696bc26296fc76116d66113656,1746165958635; _ntes_nuid=641e91696bc26296fc76116d66113656; WEVNSM=1.0.0; WNMCID=nggqzz.1746165959222.01.0; WM_TID=VTbnhbn%2BSz1BBQAAABbDLNHql9wAxhBP; ntes_utid=tid._.qimpVfcSgQtFUlUAVFOSOYG6k4hWT8Kl._.0; sDeviceId=YD-3TJia10EdYpAEgFEEAPHecH%2Fw41TSoK1; __snaker__id=kfXodLFAEWdkagVl; __remember_me=true; ntes_kaola_ad=1; timing_user_id=time_w4rIUaTLJI; __csrf=d497be3121e96997ef8bdba8faf56edb; WM_NI=PkvgzcpSIP58EU2Kdltbe3dpkI%2F%2Fr9%2B74YNaizs97HSs1sR5LSR%2F8aZ1PYAyJ6ny8bcc0vrD7BqR5F7bGVwWnIOOvObzXuOVc0an1za8E4AtFS23vfyyYeGWTIrE8PGbUHE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea8d354f3befdd2e83ba5ef8bb3d85e928b9bb0d26ef5e9fdd2c562abb5f9abb12af0fea7c3b92a94b5ba88f969b48d87b1b834878bfeace768b8beabd4e77ca997e1d0f133e9e9fcbacd6baba6bddab64491adff94d13f908d9ed0bb6b9aefa0bac4738aeaa29abb6aa1bd0097f150f59ebfb3b84ef5be89b7f65dae9781b0f545a2a69896ce5ea1f0af8fb472a3e88bd5c480868dfed4f56ebba79786c65d9897bea6bb5c85be9ba9c837e2a3; gdxidpyhxdE=HlbYtKswIqGT%2Fcu%5C842o5Bbdbn%2F1Trr5PysaDEHg%2BtrM2%2BlkXn%2FsojbO8a%5CH1AwV18bbw3%2FBRzM9yQOrrjNIgGShq6AIv7IqQzdpzuN19MjUt%2F5X6JHqIAtgq%2B4K1p7W3d6gCXeZCOwR%2BEbl617wvD5hg%2BNCVsV%2B4bYiIAyLVdMLf0LG%3A1752305891479; __csrf=70b5ed5b91b335139e178b24c02af410; MUSIC_U=005B3414382C2FF67BA7759ABB3476FD8C255CEC4239C579249870D2ACEE09B64287216DE0AE2CCF0A19360B6725016455ADF3074404A055C5ECDC9230D987EACEDA93637C24B3DD0A0F3A32C9134394B35D06BC69D4B146D6B132E7E5257591348B388CF3378880706BC9375DBF53AE8B1B3BC5D3778D8D609CEF151FE29892E14A01CFCA13F5E4EEF1AF25414D39F416D17A3101E878863A394503E76C6BE48001056B2C5746F66F33FED857DCA8F4A3221722847C46D0E34F7354058D9CDB43EF5D56E810A417ED961703079AF11699BA7E158EEB3E31F38BD299AC46CB884B4957221FABE9309672DB19AC3A83B5CE29C1B744BC1C9A19E03051E6EABA89A3F82A2BE90229CD277C2C0B2648E7CEA1AEE8D21DE27D429C8D4DDEAE9EEF34EC35C2301D040B9E3B82C5A2B23C9CDE4D45E8D08590B48AF24F2AC1CB9A7571676FAC88FB0CF7A9C3F8315106C966237992F9E9244EC3E79473BDAE054449683A; JSESSIONID-WYYY=ptFus6xJzbFT1KCOrG2eibTAln1Vz87h3EieUQDc168OB21h9fGe6NxMhIdF50xa9I75wDGJv%2BsqrrTE%2Ffzoci805AmDgfRoiQzdU%5Cw26zH4A9zGhU%5CO8OmlAhneFEoBvBEsnPplynMDJErH8nisnMAbYcEa2jcuE29OAZQvg2B7hh45%3A1752322298853'
}
def get_data(pageNo,cursor):

    with open('comment.js','r') as f:
        js_code = f.read()
    # 编译JS代码
    js = execjs.compile(js_code)
    # 调用JS中的get_comment函数
    result = js.call('get_comment',pageNo,cursor)
    # 表单参数（已逆向出的加密数据）
    params = {
        'params': result['params'],
        'encSecKey': result['encSecKey']
    }
    # 发送POST请求
    response = requests.post(url=url, data=params, headers=headers)
    # 打印响应结果
    data = response.json()['data']['comments']
    for item in data:
        name = item['user']['nickname']
        comment = item['content']
        print({"用户":name,"内容":comment})
    # 获取下一页
    cursor = response.json()['data']['cursor']
    return cursor

cursor = None
for pageNo in range(1,4):
    print(f'正在采集第{pageNo}页数据')
    cursor = get_data(pageNo,cursor)

