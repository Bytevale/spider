from DrissionPage import ChromiumPage
from datetime import datetime
import pymongo
import time
import random

dp = ChromiumPage()

# 打开目标网页
dp.get(
    'https://www.xiaohongshu.com/search_result?keyword=%25E8%258B%25B1%25E8%25AF%25AD%25E5%25AD%25A6%25E4%25B9%25A0%25E6%259C%25BA&source=web_explore_feed&type=51')

note_ids = [
    "67da1b4c000000000e007635",
    "66c5bec8000000001d017939",
    "67e037c6000000000e007023"
]
tokens = {
    "67da1b4c000000000e007635": "AB46ycdpPzxgLxk4hdJanax8MshQLaVCnT9UbNKhTKM1I%3D",
    "66c5bec8000000001d017939": "ABefO6shTCYSAhOjC5faPSW3JuPibeYsoOLcMT6f6Z5qU%3D",
    "67e037c6000000000e007023": "ABFFieW2bRRc_EKdunOUs9KJwp5fvekgIab0fRUq_l3Fs%3D"
}

# ==== 如果你想从某个页面提取 xsec_token 而非硬编码，可以启用以下代码 ====
# 打开目标详情页
# dp.get(f'https://www.xiaohongshu.com/detail/{note_ids[0]}')

# 等待 JavaScript 变量加载完成（DrissionPage 方式）
start_time = time.time()
xsec_token = None
while time.time() - start_time < 30:  # 最多等待30秒
    try:
        xsec_token = dp.run_js("return window._xsec_token")
        if xsec_token is not None:
            break
    except Exception as e:
        print(f"等待 _xsec_token 中发生异常：{e}")
    time.sleep(1)
if xsec_token is None:
    print("等待 _xsec_token 超时，使用默认值")
    xsec_token = "AB46ycdpPzxgLxk4hdJanaxxaX4BX6GaddnoYmE_brxeE%3D"

print(f"获取到的 xsec_token: {xsec_token}")


# 函数：提取并保存评论数据
def fetch_and_save_comments(note_id, token):
    # 开始监听评论接口
    dp.listen.start('comment/page')
    dp.get(f'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={note_id}&cursor=&top_comment_id=&image_formats=jpg,webp,avif&xsec_token={token}')
    r = dp.listen.wait()
    json_data = r.response.body
    print(f"API 返回数据（{note_id}）：", json_data)  # 新增调试输出，查看真实返回内容

    # 检查数据结构是否符合预期
    if isinstance(json_data, dict) and 'data' in json_data and 'comments' in json_data['data']:
        comments = json_data['data']['comments']
    else:
        print(f"数据结构异常（{note_id}），跳过该视频")
        return

    # 连接MongoDB数据库
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["spider"]
    collection = db["小红书"]

    for index in comments:
        key_list = [i for i in index.keys()]
        t = str(index['create_time'])[:-3]
        date = str(datetime.fromtimestamp(int(t)))

        # 构造用户主页 URL
        user_profile_url = f'https://www.xiaohongshu.com/user/profile/{index["user_info"]["user_id"]}?xsec_token={token}&xsec_source=pc_comment'
        dp.get(user_profile_url)
        time.sleep(2)  # 等待页面加载

        # 提取小红书号和 IP
        try:
            dp.wait(5)  # 等待页面加载完成
            xhs_id_element = dp.ele('xpath=//span[@class="user-redId"]')
            xhs_id = xhs_id_element.text if xhs_id_element else "Unknown"

            ip_element = dp.ele('xpath=//span[@class="user-IP"]')
            ip_location = ip_element.text if ip_element else "Unknown"

        except Exception as e:
            xhs_id = "Unknown"
            ip_location = "Unknown"
            print(f"⚠️ 页面解析失败: {e}")

        dit = {
            'name': index['user_info']['nickname'],
            'date': date,
            'content': index['content'],
            'xhs_id': xhs_id,          # 小红书号
            'ip': ip_location,          # 使用 XPath 提取的 IP
            'sub_content': index['sub_comments'][0]['content'] if len(index['sub_comments']) > 0 else ''
        }
        print(dit)

        # 插入数据到MongoDB（可取消注释以启用实际写入）
        collection.insert_one(dit)

    # 关闭 MongoDB 连接
    client.close()



# 主循环：遍历所有视频 ID 并采集评论
for note_id in note_ids:
    token = tokens[note_id]
    try:
        fetch_and_save_comments(note_id, token)
    except Exception as e:
        print(f"采集视频 {note_id} 失败：{e}")
    # 添加随机延迟，防止被反爬机制识别
    time.sleep(random.uniform(3, 8))