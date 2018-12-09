# -*- coding: utf-8 -*-
"""
Created on 2018/9/29 22:11

@author: dmyan
"""
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
if __name__ == '__main__':
    dataset = api.load("text8")
    dct = Dictionary(dataset)
    corpus = [dct.doc2bow(line) for line in dataset]
    model = TfidfModel(corpus)
    vector = model(corpus)
    print(vector)

