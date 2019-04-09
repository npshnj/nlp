# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 13:23:39 2018

@author: eryao
"""

import jieba
import re
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei']

def sentSeg(sentence,punctuation):
    """
    用途：断句
    输入：
        sentence:长句
        punctuation:用于断句的标点,以字符串形式输入
    输出：短句
    """
    return re.split(punctuation,sentence)

def sent2word(sentence,stopWords):
    """
    用途：分词
    输入：句子
    输出：一个已分词的list
    """
    
    #分词引擎为jieba
    segList=jieba.cut(sentence)
    segResult=[]
    for w in segList:
        segResult.append(w)
    newSent=[]
    for word in segResult:
        #判断停用词是否在句中
        if word in stopWords:
            continue
        else:
            newSent.append(word)
    return newSent

def remove_punctuation(line,strip_all=True):
    """
    用途：清洗标点
    输入：
        line:给定字符串
        strip_all：是否清洗所有标点，缺省值为True
    输出：清洗过后的字符串
    """
    if strip_all:
        #删除除中文，英文，数字，希腊字母以外的所有字符
        rule=re.compile(u"[^0-9a-zA-Z\u4e00-\u9fa5]")
        line=rule.sub('',line)
    else:
        #自定义需要删除的标点符号
        punctuation="""！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""
        re_punctuation="[{}]".format(punctuation)
        line=re.sub(re_punctuation,"",line)
    return line.strip()






def freqStats(segDataFrame,columnList,keyword,excludedList='None',minNumWords=2):
    """
    用途：统计文本词频
    输入：
        segDataFrame:已分词后的文本，以DataFrame形式存储
        columnList:需要列入统计词频的列，以list形式存储
        excludedList：需要在词频统计时排除的词表，以list形式存储,缺省值为None
        keyword:分组的关键字
        minNumWords:词的最小长度，缺省为0
    输出：以关键词分组的词频统计
    """
    
    #分词过后的文本按关键词合并
    wordVec=pd.DataFrame({clmn:segDataFrame.groupby(keyword)[clmn].agg(sum) for clmn in columnList})
    wordVec['total']=wordVec[columnList].sum(axis=1)
    wordList=list(pd.unique(segDataFrame[keyword]))
    
    #统计词频
    freqKeyword={brand:pd.Series.value_counts(wordVec.loc[brand,'详细内容']) for brand in wordList}
    for word in wordList:
        freqKeyword[word].index.name='Word'
        freqKeyword[word].rename('Frequency',inplace=True)
    for word in wordList:
        freqKeyword[word].drop(freqKeyword[word].index[[len(freqKeyword[word].index[i])<=minNumWords-1 for i
                        in range(len(freqKeyword[word].index))]],inplace=True)
    #删除excludedList中的词汇
    if excludedList=='None':
        return freqKeyword
    else:
        for word in excludedList:
            for brand in wordList:
                if word in freqKeyword[brand].index:
                    freqKeyword[brand].drop(word,inplace=True)
                else:
                    continue
        return freqKeyword
    
    

    