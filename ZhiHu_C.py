import os
import requests
from http.cookies import SimpleCookie
from fake_useragent import UserAgent
import random
import pandas as pd
import json
import brotli
import time
from pandas.io.json import json_normalize


class Volume:
    def __init__(self, keyword, path, sleeptime, tab):
        #定义搜索关键词list
        self.keyword=keyword
        #定义爬取结果储存路径
        self.path = path
        #定义请求网页间隔时间
        self.sleeptime = sleeptime
        #定义搜索的入口tab类型
        self.tab = tab
   
    def CreatePath(self):
        isExists=os.path.exists(self.path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            os.makedirs(self.path) 
            print(self.path+'  创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(self.path+'  目录已存在')
            return False    
        
    def ZhihuMain(self):
        cookie_string='''_xsrf=gvMmi39LtnwK60JM8CYVceN6IatEZdI7; _zap=939df42c-9eca-41db-b5d3-a1527b3a17ff; d_c0="ADCiGnxNzg6PTvbksJWvVmZFpFM3O3KmHSY=|1547142906"; q_c1=dbd4e3fbaeb14e629eb7432289ab8cca|1553082206000|1547142983000; tst=r; capsion_ticket="2|1:0|10:1553081233|14:capsion_ticket|44:MWJhOGQ4NGQyYmNmNGU1NTg4YWI0ZTA1ZDc4NjliYTk=|007d490dae3c26eea075890aec2e8f65b28925856f0fb923480829140dffb007"; tgw_l7_route=4860b599c6644634a0abcd4d10d37251'''
        sc=SimpleCookie(cookie_string)
        cookies={v.key:v.value for k,v in sc.items()}
        #定义headers
        headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        #初始化params
        #url初始化
        #log及输出list初始化
        spider_log=[]
        keylist=self.keyword
        tablist=self.tab
        for tab in tablist:
            result_dflist=[]
            for keyword in keylist:
                url='https://api.zhihu.com/search_v3?advert_count=0&correction=1&limit=20&offset=0&q='+keyword+'&t='+tab+'&show_all_topics=0'
                numScc=0
                search_object=[]
                #提取搜索关键词list下的所有结果
                for i in range(1000000):
                    response = requests.get(url, headers=headers,cookies=cookies)
                    response.encoding='gzip'
                    html = response.text
                    if len(json.loads(html)['data'])==0:
                        print(f"For tab- {tab},keyword- {keyword}, page {i} finished, {numScc} records")
                        spider_log.append(f"For tab- {tab},keyword- {keyword}, page {i} finished, {numScc} records")
                        break
                    else:
                        r_dict=json.loads(html)['data']
                        search_object.append(r_dict)
                        numScc=numScc+len(r_dict)
                        if json.loads(html)['paging']['is_end']==False:
                            #url重置化
                            url=json.loads(html)['paging']['next']
                        else:
                            print(f"Page {i+1} finished, {numScc} records")
                            spider_log.append(f"Page {i+1} finished, {numScc} records")
                    time.sleep(self.sleeptime)
                #解析成df并设置为keywordlevel
                dfs=[]
                for one in search_object:
                    dfs.append(json_normalize(one))
                result=pd.concat(dfs)
                result['keyword'] =keyword
                result['tab'] =tab
                result.reset_index(drop=True) 
                result_dflist.append(result)             
            result_df=pd.concat(result_dflist)
            result_df.reset_index(drop=True) 
            #输出文件至指定路径下
            lib=self.path+tab+".csv"
            result_df.to_csv(lib,encoding='utf-8')
        return result_df

