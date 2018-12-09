# -*- coding: utf-8 -*-
"""
Created on 18-9-30 上午11:01

@author: dmyan
"""
import jieba

class Seg(object):
    stopwords = []
    stopword_filepath = 'data/stopword.txt'
    def __init__(self):
        pass

    def cut(self,sentence):
        seg_list = ' '.join(jieba.cut(sentence.strip())).split()
        return seg_list
    def cut_for_search(self,sentence):
        seg_list = ' '.join(jieba.cut_for_search(sentence.strip())).split()
        return seg_list

if __name__ == '__main__':
    pass