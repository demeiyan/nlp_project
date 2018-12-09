# -*- coding: utf-8 -*-
"""
Created on 18-9-30 上午11:15

@author: dmyan
"""
from sentence_search.cutWords import *
from gensim import corpora, models, similarities

from sentence_search.sentences import Sentence


class SentenceSimilarity():

    def __init__(self, sententce_token_list):
        self.token_list = sententce_token_list

    def simple_model(self):
        self.dictionary = corpora.Dictionary(self.token_list)
        self.corpus_simple = [self.dictionary.doc2bow(token) for token in self.token_list]


    # tfidf model
    def TfidfModel(self):
        self.simple_model()

        self.model = models.TfidfModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]

        self.index = similarities.MatrixSimilarity(self.corpus)

    # lsi model
    def LsiModel(self):
        self.simple_model()

        self.model = models.LsiModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]

        self.index = similarities.MatrixSimilarity(self.corpus)

    # lda model
    def LdaModel(self):
        self.simple_model()

        self.model = models.LdaModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]

        self.index = similarities.MatrixSimilarity(self.corpus)

    def sentence2vec(self,sentence):
        sentence = Sentence(sentence)
        vec_bow = self.dictionary.doc2bow(sentence.get_cuted_token_list()[0])
        return self.model[vec_bow]

    def similarity(self, sentence):
        sentence_vec = self.sentence2vec(sentence)
        sims = self.index[sentence_vec]

        cand3 = []

        sim_sort = sorted(list(enumerate(sims)),key=lambda item:item[1], reverse=True)

        index,score = sim_sort[0][0],sim_sort[0][1]
        # print('score====',score)
        cand_index1 = index - 1
        cand_index2 = index + 1

        if index == 0:
            cand_index1 = index + 2


        cand3.append(''.join(self.token_list[index]))
        if cand_index1 < len(self.token_list) and cand_index1>=0:
            cand3.append(''.join(self.token_list[cand_index1]))
        if cand_index2 < len(self.token_list) and cand_index2 >= 0:
            cand3.append(''.join(self.token_list[cand_index2]))

        # return ''.join(self.token_list[index])
        return cand3, score

if __name__ == '__main__':
    pass