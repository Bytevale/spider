import re
from DrissionPage import ChromiumPage
import datetime
from pymongo import MongoClient
import random
import time

# 连接到 MongoDB
client = MongoClient('127.0.0.1', 27017)  # 根据你的 MongoDB 配置修改连接字符串
db = client['spider']  # 使用 'spider' 数据库
collection = db['知乎']  # 使用 '知乎' 集合


# 清洗 HTML 标签的函数
def remove_html_tags(text):
    if not text:
        return "Unknown"
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# 定义要搜索的话题列表
topics = [
    '大学生社交',
    '大学生社交技巧',
    '大学生社交焦虑',
    '大学生社交的建议',
    '大学生社交的现状',
    '大学生社交场所'
]

cp = ChromiumPage()

for topic in topics:
    print(f"正在采集话题: {topic}")
    search_url = f'https://www.zhihu.com/search?q={topic}&search_source=History&utm_content=search_history&type=content'
    cp.get(search_url)
    cp.listen.start('api/v4/search_v3')

    previous_height = cp.run_js('return document.body.scrollHeight')
    no_new_content_count = 0  # 新增计数器，防止误判

    for page in range(1500):
        cp.scroll.to_bottom()
        time.sleep(2)

        new_height = cp.run_js('return document.body.scrollHeight')
        if new_height == previous_height:
            no_new_content_count += 1
            print(f"未检测到新内容，已连续{no_new_content_count}次无变化")
            if no_new_content_count >= 3:  # 连续3次无变化才判定为到底
                print("已经到达页面底部，切换话题。")
                break  # 结束当前话题循环
        else:
            no_new_content_count = 0
            previous_height = new_height

        try:
            resp = cp.listen.wait(timeout=10)
            if not resp:  # 如果 resp 是 False，说明超时或未捕获到请求
                print("未监听到接口请求，跳过本次循环")
                continue

            json_data = resp.response.body
        except Exception as e:
            print(f"监听或解析响应失败：{e}")
            continue

        data_list = json_data.get('data', [])
        for item in data_list:
            try:
                # 提取并清洗标题
                title = remove_html_tags(item.get('highlight', {}).get('title', 'Unknown'))

                # 提取内容并清洗
                object_data = item.get('object', {})
                content = remove_html_tags(object_data.get('content', 'Unknown'))

                # 提取并格式化时间
                created_time = object_data.get('created_time', None)
                if created_time:
                    created_time_str = datetime.datetime.fromtimestamp(created_time).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    created_time_str = '未知时间'

                # 创建要插入的文档
                document = {
                    '话题': topic,
                    '标题': title,
                    '内容': content,
                    '发布时间': created_time_str,
                }

                # 打印清洗后的数据
                print(f"话题: {topic}")
                print(f"标题: {title}")
                print(f"内容: {content}")
                print(f"发布时间: {created_time_str}")
                print("-" * 50)

                # 插入到 MongoDB
                collection.insert_one(document)

            except Exception as e:
                print(f"处理数据时出错: {e}")

        # 随机延迟，避免请求过于频繁
        time.sleep(random.randint(1, 2))

# 关闭 MongoDB 连接
client.close()
