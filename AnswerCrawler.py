# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 19:21:56 2019

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
from math import ceil

cookie_string='''_xsrf=gvMmi39LtnwK60JM8CYVceN6IatEZdI7; _zap=939df42c-9eca-41db-b5d3-a1527b3a17ff; d_c0="ADCiGnxNzg6PTvbksJWvVmZFpFM3O3KmHSY=|1547142906"; q_c1=dbd4e3fbaeb14e629eb7432289ab8cca|1553082206000|1547142983000; tst=r; capsion_ticket="2|1:0|10:1553081233|14:capsion_ticket|44:MWJhOGQ4NGQyYmNmNGU1NTg4YWI0ZTA1ZDc4NjliYTk=|007d490dae3c26eea075890aec2e8f65b28925856f0fb923480829140dffb007"; tgw_l7_route=a37704a413efa26cf3f23813004f1a3b'''
sc=SimpleCookie(cookie_string)
cookies={v.key:v.value for k,v in sc.items()}

column_list_question=['q_create_time','qid','q_type','q_title','q_url','created_time']
question_dataframe=pd.read_csv('target_question_rest.csv',sep=',',encoding='utf-8',usecols=column_list_question)
question_list=question_dataframe['qid'].tolist()

headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Encoding':'gzip, deflate, br',
         'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
         'Connection':'keep-alive',
         'DNT':'1',
         'Host':'www.zhihu.com',
         'TE':'Trailer',
         'Upgrade-Insecure-Requests':'1',
         'User-Agent':UserAgent().random
        }

parse_params={'include':'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
              'limit':'5',
              'offset':'0',
              'platform':'desktop',
              'sort_by':'default'
        }


#variables for crawlers to capture
ans_id,ans_admin_closed_comment,ans_annoation_action,ans_type,author_badge,\
author_follower_count,author_gender,author_headline,author_id,author_is_advertiser,\
author_is_org,author_is_privacy,author_name,author_type,author_url,author_url_token,\
ans_can_comment_reason,ans_can_comment_status,ans_collapse_reason,ans_collapsed_by,\
ans_comment_count,ans_comment_permission,ans_content,ans_created_time,\
ans_editable_content,ans_extra,ans_is_collapsed,ans_is_copyable,ans_is_labled,\
ans_is_normal,ans_is_sticky,ans_mark_infos,ans_is_relevant,ans_relevant_text,\
ans_relevent_type,ans_reshipment_setting,ans_can_open_reward,ans_is_rewardable,\
ans_reward_member_count,ans_reward_total_money,ans_tagline,ans_suggest_edit_reason,\
ans_suggest_edit_status,ans_suggest_edit_tip,ans_suggest_edit_title,ans_suggest_edit_url,\
ans_updated_time,ans_url,ans_voteup_count,q_id=[],[],[],[],[],[],[],[],[],[],[],[],\
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],\
[],[],[],[],[],[],[],[],[],[],[],[]

#iterate over question list to capture answers
for qid in question_list:
    url=f"https://www.zhihu.com/api/v4/questions/{qid}/answers"
    pages_num=10000
    i=0
    while i<pages_num:
        numScc=0
        numFlr=0
        #randomize user-agent
        headers['User-Agent']=UserAgent().random
        #turn over pages
        parse_params['offset']=str(i*5)
        with requests.Session() as s:
            r=s.get(url,params=parse_params,headers=headers,cookies=cookies)
        #Deal with brotli encoding
        decprs_stream=brotli.decompress(r.content)
        stream_decode=decprs_stream.decode('utf-8')
        pages_num=ceil(json.loads(stream_decode)['paging']['totals']/5)
        ans_data=json.loads(stream_decode)['data']
        #data loading
        for data in ans_data:
            try:
                ans_id.append(data['id'])
                numScc+=1
            except:
                ans_id.append('NULL')
                numFlr+=1
            try:
                ans_admin_closed_comment.append(data['admin_closed_comment'])
            except:
                ans_admin_closed_comment.append('NULL')
            try:
                ans_annoation_action.append(data['annotation_action'])
            except:
                ans_annoation_action.append('NULL')
            try:
                ans_type.append(data['answer_type'])
            except:
                ans_type.append('NULL')
            try:
                author_badge.append(data['author']['badge'])
            except:
                author_badge.append('NULL')
            try:
                author_follower_count.append(data['author']['follower_count'])
            except:
                author_follower_count.append('NULL')
            try:
                author_gender.append(data['author']['gender'])
            except:
                author_gender.append('NULL')
            try:
                author_headline.append(data['author']['headline'])
            except:
                author_headline.append('NULL')
            try:
                author_id.append(data['author']['id'])
            except:
                author_id.append('NULL')
            try:
                author_is_advertiser.append(data['author']['is_advertiser'])
            except:
                author_is_advertiser.append('NULL')
            try:
                author_is_org.append(data['author']['is_org'])
            except:
                author_is_org.append('NULL')
            try:
                author_is_privacy.append(data['author']['is_privacy'])
            except:
                author_is_privacy.append('NULL')
            try:
                author_name.append(data['author']['name'])
            except:
                author_name.append('NULL')
            try:
                author_type.append(data['author']['type'])
            except:
                author_type.append('NULL')
            try:
                author_url.append(data['author']['url'])
            except:
                author_url.append('NULL')
            try:
                author_url_token.append(data['author']['url_token'])
            except:
                author_url_token.append('NULL')
            try:
                ans_can_comment_reason.append(data['can_comment']['reason'])
            except:
                ans_can_comment_reason.append('NULL')
            try:
                ans_can_comment_status.append(data['can_comment']['status'])
            except:
                ans_can_comment_status.append('NULL')
            try:
                ans_collapse_reason.append(data['collapse_reason'])
            except:
                ans_collapse_reason.append('NULL')
            try:
                ans_collapsed_by.append(data['collapsed_by'])
            except:
                ans_collapsed_by.append('NULL')
            try:
                ans_comment_count.append(data['comment_count'])
            except:
                ans_comment_count.append('NULL')
            try:
                ans_comment_permission.append(data['comment_permission'])
            except:
                ans_comment_permission.append('NULL')
            try:
                ans_content.append(data['content'])
            except:
                ans_content.append('NULL')
            try:
                ans_created_time.append(data['created_time'])
            except:
                ans_created_time.append('NULL')
            try:
                ans_editable_content.append(data['editable_content'])
            except:
                ans_editable_content.append('NULL')
            try:
                ans_extra.append(data['extra'])
            except:
                ans_extra.append('NULL')
            try:
                ans_is_collapsed.append(data['is_collapsed'])
            except:
                ans_is_collapsed.append('NULL')
            try:
                ans_is_copyable.append(data['is_copyable'])
            except:
                ans_is_copyable.append('NULL')
            try:
                ans_is_labled.append(data['is_labeled'])
            except:
                ans_is_labled.append('NULL')
            try:
                ans_is_normal.append(data['is_normal'])
            except:
                ans_is_normal.append('NULL')
            try:
                ans_is_sticky.append(data['is_sticky'])
            except:
                ans_is_sticky.append('NULL')
            try:
                ans_mark_infos.append(data['mark_infos'])
            except:
                ans_mark_infos.append('NULL')
            try:
                ans_is_relevant.append(data['relevant_info']['is_relevant'])
            except:
                ans_is_relevant.append('NULL')
            try:
                ans_relevant_text.append(data['relevant_info']['relevant_text'])
            except:
                ans_relevant_text.append('NULL')
            try:
                ans_relevent_type.append(data['relevant_info']['relevant_type'])
            except:
                ans_relevent_type.append('NULL')
            try:
                ans_reshipment_setting.append(data['reshipment_settings'])
            except:
                ans_reshipment_setting.append('NULL')
            try:
                ans_can_open_reward.append(data['reward_info']['can_open_reward'])
            except:
                ans_can_open_reward.append('NULL')
            try:
                ans_is_rewardable.append(data['reward_info']['is_rewardable'])
            except:
                ans_is_rewardable.append('NULL')
            try:
                ans_reward_member_count.append(data['reward_info']['reward_member_count'])
            except:
                ans_reward_member_count.append('NULL')
            try:
                ans_reward_total_money.append(data['reward_info']['reward_total_money'])
            except:
                ans_reward_total_money.append('NULL')
            try:
                ans_tagline.append(data['reward_info']['tagline'])
            except:
                ans_tagline.append('NULL')
            try:
                ans_suggest_edit_reason.append(data['suggest_edit']['reason'])
            except:
                ans_suggest_edit_reason.append('NULL')
            try:
                ans_suggest_edit_status.append(data['suggest_edit']['status'])
            except:
                ans_suggest_edit_status.append('NULL')
            try:
                ans_suggest_edit_tip.append(data['suggest_edit']['tip'])
            except:
                ans_suggest_edit_tip.append('NULL')
            try:
                ans_suggest_edit_title.append(data['suggest_edit']['title'])
            except:
                ans_suggest_edit_title.append('NULL')
            try:
                ans_suggest_edit_url.append(data['suggest_edit']['url'])
            except:
                ans_suggest_edit_url.append('NULL')
            try:
                ans_updated_time.append(data['updated_time'])
            except:
                ans_updated_time.append('NULL')
            try:
                ans_url.append(data['url'])
            except:
                ans_url.append('NULL')
            try:
                ans_voteup_count.append(data['voteup_count'])
            except:
                ans_voteup_count.append('NULL')
            q_id.append(qid)
        i+=1
        print(f"Page {i} finished, {numScc} successes, {numFlr} failuares")
        time.sleep(random.randint(25,30))
            
                
column_list_ans=['ans_id','ans_admin_closed_comment','ans_annoation_action','ans_type','author_badge',\
'author_follower_count','author_gender','author_headline','author_id','author_is_advertiser',\
'author_is_org','author_is_privacy','author_name','author_type','author_url','author_url_token',\
'ans_can_comment_reason','ans_can_comment_status','ans_collapse_reason','ans_collapsed_by',\
'ans_comment_count','ans_comment_permission','ans_content','ans_created_time',\
'ans_editable_content','ans_extra','ans_is_collapsed','ans_is_copyable','ans_is_labled',\
'ans_is_normal','ans_is_sticky','ans_mark_infos','ans_is_relevant','ans_relevant_text',\
'ans_relevent_type','ans_reshipment_setting','ans_can_open_reward','ans_is_rewardable',\
'ans_reward_member_count','ans_reward_total_money','ans_tagline','ans_suggest_edit_reason',\
'ans_suggest_edit_status','ans_suggest_edit_tip','ans_suggest_edit_title','ans_suggest_edit_url',\
'ans_updated_time','ans_url','ans_voteup_count','q_id']
#load data into the frame
ans_DataFrame=pd.DataFrame({clmn:eval(clmn) for clmn in column_list_ans})
#ans_DataFrame.to_csv('ans700_800_rest.csv',sep=',',encoding='utf-8',index=False)  
#test=pd.read_csv('ans700_800_rest.csv',sep=',',encoding='utf-8',usecols=column_list_ans)