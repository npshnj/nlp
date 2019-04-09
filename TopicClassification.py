# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 10:24:05 2019

@author: eryao
"""

import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.cluster import KMeans
from sentimentanalysis import sent2word,remove_punctuation

#load user-defined dictionary
jieba.load_userdict('user.txt')
stopWordsList=open('stopwords.txt','r',encoding='utf-8')
stopWords=[line.split('\n')[0] for line in stopWordsList.readlines()]
stopWordsList.close()

parser=lambda date:pd.to_datetime(date,unit='s')
zhq_df=pd.read_csv('target_question.csv',sep=',',encoding='utf-8',parse_dates=['q_create_time'],date_parser=parser)

#word segmentation
column_for_seg_zh=['q_title']
zhq_df.update(pd.DataFrame({clmn:list(sent2word(remove_punctuation
                        (sentce,strip_all=True),stopWords) for sentce in zhq_df[clmn])
                        for clmn in column_for_seg_zh}))

#collapse the synonyms into one
zhq_df['q_title_clean']=zhq_df['q_title'].apply(lambda x:['intel' if y=='Intel'\
      or y=='英特尔' or y=='INTEL' else 'ryzen' if y=='Ryzen' or y=='RYZEN' else\
      'CPU' if y=='处理器' or y=='cpu' else 'AMD' if y=='amd' \
      else '七代' if y=='7代' else y for y in x])

q_str_list=zhq_df['q_title_clean'].tolist()
q_str_list_space=[' '.join(ele) for ele in q_str_list]
#create tf-idf vectors
vectorizer=CountVectorizer()
transformer=TfidfTransformer()
tfidf=transformer.fit_transform(vectorizer.fit_transform(q_str_list_space))
word=vectorizer.get_feature_names()
weight=tfidf.toarray()

#kmeans clustering(4-cluster)
km_cluster=KMeans(n_clusters=4,max_iter=10000,n_init=1000,init='k-means++',n_jobs=-1)
km_cluster.fit(weight)
label_pred = km_cluster.labels_.tolist()
label_DataFrame=pd.DataFrame({'qid':zhq_df['qid'].tolist(),'q_title':zhq_df['q_title'].tolist(),'q_created_time':zhq_df['q_create_time'].tolist(),'label':label_pred})
zhq_df_label=pd.merge(zhq_df,label_DataFrame,on='qid')
zhq_df_clus1,zhq_df_clus2,zhq_df_clus3,zhq_df_clus4=(zhq_df_label.query(f'label=={i}') for i in range(4))