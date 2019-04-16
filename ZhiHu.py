# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 22:28:08 2019

@author: daozh
"""

import requests
from http.cookies import SimpleCookie
from fake_useragent import UserAgent
import random
import pandas as pd
import json
import brotli
import time




cookie_string='''_xsrf=gvMmi39LtnwK60JM8CYVceN6IatEZdI7; _zap=939df42c-9eca-41db-b5d3-a1527b3a17ff; d_c0="ADCiGnxNzg6PTvbksJWvVmZFpFM3O3KmHSY=|1547142906"; q_c1=dbd4e3fbaeb14e629eb7432289ab8cca|1553082206000|1547142983000; tst=r; capsion_ticket="2|1:0|10:1553081233|14:capsion_ticket|44:MWJhOGQ4NGQyYmNmNGU1NTg4YWI0ZTA1ZDc4NjliYTk=|007d490dae3c26eea075890aec2e8f65b28925856f0fb923480829140dffb007"; tgw_l7_route=4860b599c6644634a0abcd4d10d37251'''
sc=SimpleCookie(cookie_string)
cookies={v.key:v.value for k,v in sc.items()}

headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Accept-Encoding':'gzip,deflate,br',
         'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
         'Connection':'keep-alive',
         'Cookie':cookie_string,
         'DNT':'1',
         'Host':'www.zhihu.com',
         'Referer':'https://www.zhihu.com/topic/19552747/top-answers',
         'TE':'Trailer',
         'Upgrade-Insecure-Requests':'1',
         'User-Agent':UserAgent().random
         }

parse_params={'include':'data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;',
              'limit':'10',
              'offset':'950'
        }

#url1='https://www.zhihu.com/api/v4/topics/19552747/feeds/essence?include=data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=topic_sticky_module)].target.data[?(target.type=answer)].target.is_normal,comment_count,voteup_count,content,relevant_info,excerpt.author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=article)].target.content,voteup_count,comment_count,voting,author.badge[?(type=best_answerer)].topics;data[?(target.type=topic_sticky_module)].target.data[?(target.type=people)].target.answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics;data[?(target.type=answer)].target.annotation_detail,content,hermes_label,is_labeled,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[?(target.type=answer)].target.author.badge[?(type=best_answerer)].topics;data[?(target.type=article)].target.annotation_detail,content,hermes_label,is_labeled,author.badge[?(type=best_answerer)].topics;data[?(target.type=question)].target.annotation_detail,comment_count;&limit=10&offset=15'
url='https://www.zhihu.com/api/v4/topics/19562867/feeds/essence'
#r=requests.get(url,headers=headers,cookies=cookies,params=parse_params)
#decprs_stream=brotli.decompress(r.content)
#stream_decode=decprs_stream.decode('utf-8')
#qlist=json.loads(stream_decode)['data']

q_create_time,qid,q_type,q_title,q_url=[],[],[],[],[]
author_badge,author_member_tag,author_type,author_headline,author_gender,author_id,\
author_is_advertiser,author_is_org,author_name,author_type,author_url,\
author_url_token,author_user_type,article_comment_count,article_content,\
article_created,article_id,article_title,article_updated,article_url,\
article_voteup_count=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
spider_log=[]

for i in range(100):
    numScc=0
    numFlr=0
    parse_params['offset']=str(10*i)
    headers['User-Agent']=UserAgent().random
    with requests.Session() as s:
        r=s.get(url,params=parse_params,headers=headers,cookies=cookies)
        decprs_stream=brotli.decompress(r.content)
        stream_decode=decprs_stream.decode('utf-8')
        qlist=json.loads(stream_decode)['data']
        for content in qlist:
            if content['target']['type']=='answer':
                try:
                    qid.append(content['target']['question']['id'])
                    numScc+=1
                except:
                    qid.append('NULL')
                    numFlr+=1
                try:
                    q_create_time.append(content['target']['question']['created'])
                except:
                    q_create_time.append('NULL')
                try:
                    q_type.append(content['target']['question']['type'])
                except:
                    q_type.append('NULL')
                try:
                    q_title.append(content['target']['question']['title'])
                except:
                    q_title.append('NULL')
                try:
                    q_url.append(content['target']['question']['url'])
                except:
                    q_url.append('NULL')
            elif content['target']['type']=='article':
                try:
                    article_id.append(content['target']['id'])
                    numScc+=1
                except:
                    article_id.append('NULL')
                    numFlr+=1
                try:
                    author_badge.append(content['target']['author']['badge'])
                except:
                    author_badge.append('NULL')
                try:
                    author_member_tag.append(content['target']['author']['edu_member_tag']['member_tag'])
                except:
                    author_member_tag.append('NULL')
                try:
                    author_type.append(content['target']['author']['edu_member_tag']['type'])
                except:
                    author_type.append('NULL')
                try:
                    author_headline.append(content['target']['author']['headline'])
                except:
                    author_headline.append('NULL')
                try:
                    author_gender.append(content['target']['author']['gender'])
                except:
                    author_gender.append('NULL')
                try:
                    author_id.append(content['target']['author']['id'])
                except:
                    author_id.append('NULL')
                try:
                    author_is_advertiser.append(content['target']['author']['is_advertiser'])
                except:
                    author_is_advertiser.append('NULL')
                try:
                    author_is_org.append(content['target']['author']['is_org'])
                except:
                    author_is_org.append('NULL')
                try:
                    author_name.append(content['target']['author']['name'])
                except:
                    author_name.append('NULL')
                try:
                    author_url.append(content['target']['author']['url'])
                except:
                    author_url.append('NULL')
                try:
                    author_url_token.append(content['target']['author']['url_token'])
                except:
                    author_url_token.append('NULL')
                try:
                    author_user_type.append(content['target']['author']['user_type'])
                except:
                    author_user_type.append('NULL')
                try:
                    article_comment_count.append(content['target']['comment_count'])
                except:
                    article_comment_count.append('NULL')
                try:
                    article_content.append(content['target']['content'])
                except:
                    article_content.append('NULL')
                try:
                    article_created.append(content['target']['created'])
                except:
                    article_created.append('NULL')
                try:
                    article_title.append(content['target']['title'])
                except:
                    article_title.append('NULL')
                try:
                    article_updated.append(content['target']['updated'])
                except:
                    article_updated.append('NULL')
                try:
                    article_url.append(content['target']['url'])
                except:
                    article_url.append('NULL')
                try:
                    article_voteup_count.append(content['target']['voteup_count'])
                except:
                    article_voteup_count.append('NULL')
    print(f"Page {i} finished, {numScc} successes, {numFlr} failuares")
    spider_log.append(f"Page {i} finished, {numScc} successes, {numFlr} failuares")
    time.sleep(random.randint(25,30))
                
                    
#columnList1=['q_create_time','qid','q_type','q_title','q_url','created_time']
#columnList2=['author_badge','author_member_tag','author_type','author_headline','author_gender','author_id',\
#'author_is_advertiser','author_is_org','author_name','author_type','author_url',\
#'author_url_token','author_user_type','article_comment_count','article_content',\
#'article_created','article_title','article_updated','article_url',\
#'article_voteup_count','created_time','updated_time']
#qDataFrame=pd.DataFrame({clmn:eval(clmn) for clmn in columnList1})
#articleDataFrame=pd.DataFrame({clmn:eval(clmn) for clmn in columnList2})
#qDataFrame.drop_duplicates(inplace=True)
#qDataFrame['created_time']=qDataFrame['q_create_time'].apply(lambda x:time.strftime("%m/%d/%Y %H:%M:%S",time.localtime(x)))          
#articleDataFrame['created_time']=articleDataFrame['article_created'].apply(lambda x:time.strftime("%m/%d/%Y %H:%M:%S",time.localtime(x)))
#articleDataFrame['updated_time']=articleDataFrame['article_updated'].apply(lambda x:time.strftime("%m/%d/%Y %H:%M:%S",time.localtime(x)))
#qDataFrame.to_csv('CPU_questions.csv',sep=',',encoding='utf-8',index=False)
#articleDataFrame.to_csv('CPU_Articles.csv',sep=',',encoding='utf-8',index=False)
#test1=pd.read_csv('CPU_questions.csv',sep=',',encoding='utf-8',usecols=columnList1)
#test2=pd.read_csv('CPU_Articles.csv',sep=',',encoding='utf-8',usecols=columnList2)