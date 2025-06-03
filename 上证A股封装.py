import requests,time
import pymongo

class DFCFSpider:
    url = 'https://56.push2.eastmoney.com/api/qt/clist/get'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    }
    id = 1
    # 获取请求参数
    def get_params(self,page=1):
        """请求参数"""
        return {
            # 每次循环更改页码参数
            "pn": page,
            "pz": 20,
            "np": 1,
            "po": 1,
            # 上证A股的数据采集
            "fs": "m:1 t:2,m:1 t:23",
            "fid": "f3",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            '_': int(time.time() * 1000),
            "fltt": 2,
            "invt": 2,
            "dect": 1,
            "wbp2u": "|0|0|0|web"
        }
    # 解析数据
    def parser_data(self,response):
        """解析数据"""
        # 获取当前页面的所有数据
        result = response.json()
        lists = result['data']['diff']
        data_list = []
        for item in lists:
            name = item['f14']
            code = item['f12']
            gains = item['f3']
            print({"name":name,"code":code,"gains":gains})
            data_list.append({"_id":self.id,"name":name,"code":code,"gains":gains})
            self.id += 1
            return data_list
    # 连接数据库
    def link_database(self,data):
        # 连接MongoDB数据库
        client = pymongo.MongoClient('127.0.0.1',27017)
        # 选择数据库
        db = client['spider']
        # 选择集合
        a_stock1 = db["上证A股1"]
        # 存储数据
        if isinstance(data,list):
            a_stock1.insert_many(data)
        else:
            a_stock1.insert_one(data)

    # 翻页操作
    def roll_page(self,current_page):
        """翻页逻辑"""
        next_page = current_page + 1
        params = self.get_params(next_page)
        response = requests.get(url=self.url,headers=self.headers,params=params)
        return response
    # 主函数
    def main(self):
        current_page = 1
        while True:
            # 获取请求参数
            params = self.get_params(current_page)
            # 发送请求
            response = requests.get(url=self.url,headers=self.headers,params=params)
            # 解析数据
            data = self.parser_data(response)
            # 存储数据
            if data:
                self.link_database(data)

            # 检查是否有下一页
            try:
                next_response = self.roll_page(current_page)
                if not next_response.json()['data']['diff']:
                    break
                current_page += 1
                time.sleep(1) # 防止请求过于频繁
            except:
                break


# 函数的调用
DFCFSpider().main()





