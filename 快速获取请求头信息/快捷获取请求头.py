"""
步骤：
    1，创建一个txt文件，将copy的请求头信息复制进去
    2，将数据传所在的文件传入到函数中

"""

def get_headers(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        items = f.readlines()
        headers = {}
        for i in items:
            k, v = i.replace('\n', '').split(': ')
            headers[k] = v
    return headers


headers = get_headers('header.txt')
print(headers)