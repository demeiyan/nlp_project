# -*- coding: utf-8 -*-
"""
Created on 18-10-24 上午9:46

@author: dmyan
"""
import os
from nltk.parse import CoreNLPParser
import logging
import json
from nltk.parse import CoreNLPDependencyParser

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.url = host+':'+str(port)
        self.dep_parser = CoreNLPDependencyParser(self.url)
        self.nlp = CoreNLPParser(self.url)


    def word_tokenize(self, sentence):
        return self.nlp.tokenize(sentence)

    # def pos(self, sentence):
    #     sentence = self.word_tokenize(sentence)
    #     pos_tagger = CoreNLPParser(url=self.url, tagtype='pos')
    #     return pos_tagger.tag(sentence)
    #
    # def ner(self, sentence):
    #     ner_tagger = CoreNLPParser(url=self.url, tagtype='ner')
    #     return list(ner_tagger.tag(self.word_tokenize(sentence)))
    #
    # def parse(self, sentence):
    #     return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):

        parses = self.dep_parser.parse(self.word_tokenize(sentence))
        return parses

    # def annotate(self, sentence):
    #     return json.loads(self.nlp.annotate(sentence, properties=self.props))
    #     return json.loads(self.nlp.annotate(sentence, properties=self.props))


if __name__ == '__main__':
    # sentence = '美国总统是？'
    nlp = StanfordNLP()

    while True:
        sentence = query = input('输入句子:\n')
        parses = nlp.dependency_parse(sentence)
        list = [[(dep,governor[0], dependent[0]) for governor, dep, dependent in parse.triples()] for parse in parses]

        #print(nlp.pos(sentence))
        dep_list = []
        for d in list[0]:
            dep_list.append(str(d[0])+'('+str(d[1])+','+str(d[2])+')')
        # print(sentence)
        print()
        print(dep_list)
        print()


    # sentence = '马拉维市是冲突的主要地区'
    #
    # parses = nlp.dependency_parse(sentence)
    # list = [[(dep,governor[0], dependent[0]) for governor, dep, dependent in parse.triples()] for parse in parses]
    #
    #
    # dep_list = []
    # for d in list[0]:
    #     dep_list.append(str(d[0])+'('+str(d[1])+','+str(d[2])+')')
    # print(sentence)
    # print()
    # print(dep_list)



    # parser = StanfordParser('/home/dmyan/codes/github/repositories/nlp_project/question answering/text_QuestionAnswering/data/corenlp/stanford-corenlp-3.9.1.jar',model_path="data/corenlp/model/edu/stanford/models/lexparser/englishPCFG.ser.gz")
    # print(list(parser.raw_parse("the quick brown fox jumps over the lazy dog")))