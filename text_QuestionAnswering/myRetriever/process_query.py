# -*- coding: utf-8 -*-
"""
Created on 18-10-17 下午11:17

@author: dmyan
"""
import argparse
from tfidf_doc_ranker import TfidfDocRanker
# from sentence_search.getMaxSimSentence import MaxSimSentence
import warnings
import re
import numpy as np
import os
from stanfordParser import StanfordNLP
class Process(object):
    def __init__(self):
        pass

    def get_answer(self, sentence, query):

        q_words = []
        q_word = ''
        with open('./data/rawtexts/q_words.txt', 'r') as q:
            line = q.readline().strip()
            while line:
                q_words.append(line)
                line = q.readline().strip()
        isContains = False

        for w in q_words:
            if w in query:
                isContains = True
                q_word = w
                break
        dep_list = ['SUB', 'NMOD', 'OBJ']
        isFind = False
        answer = []
        if isContains:

            ref_words = None
            relation = ''
            nlp = StanfordNLP()
            q_parses = nlp.dependency_parse(query)

            for parse in q_parses:
                for governor, dep, dependent in parse.triples():
                    if dependent[0] == q_word:
                        relation = dep
                        ref_words = governor[0]
            currentWords = None

            if relation in dep_list:

                s_parses = nlp.dependency_parse(sentence)
                for parse in s_parses:
                    for governor, dep, dependent in parse.triples():
                        if governor[0] == ref_words and dep == relation:
                            isFind = True
                            currentWords = dependent[0]
                            answer.append(currentWords)
                        if currentWords != None and dep == 'NMOD' and governor[0] == currentWords:
                            answer.append(dependent[0])
                            currentWords = dependent[0]
                if isFind:
                    answer.reverse()

                    return ''.join(answer)

        return LCS_Answer(sentence, query)

def last_index(content,c):
    cnt = 0
    i = 0
    for char in content:
        if char == c:
            cnt = i
        i += 1
    return cnt

def maxSubstring(answer_content,question):

    answer_content_len = len(answer_content)
    question_len = len(question)

    if question_len == 0 or answer_content_len ==0:
        return ''

    for i in range(question_len):
        begin = 0
        for end in range(question_len-i,question_len+1):
            current = question[begin:end]
            if current in answer_content:
                return current
            begin += 1
    return ''


def LCS_Answer(content,question):

    r = 0
    l = 0
    ansvalue = 0
    content_len = len(content)
    question_len = len(question)
    dp = np.zeros((content_len+1,question_len+1),dtype=int)
    for i in range(1,content_len+1):
        for j in range(1, question_len+1):
            dp[i][j] = np.maximum(dp[i-1][j],dp[i][j-1])
            if content[i-1] == question[j-1]:
                dp[i][j] = np.maximum(dp[i][j],dp[i-1][j-1]+1)
            ansvalue = np.maximum(ansvalue,dp[i][j])

    for i in range(1,content_len+1):
        if dp[i][question_len] == ansvalue:
            r = i - 1
            break

    dp = np.zeros((content_len + 2, question_len + 2), dtype=int)
    for i in range(content_len,0,-1):
        for j in range(question_len,0,-1):
            dp[i][j] = np.maximum(dp[i + 1][j], dp[i][j + 1])
            if content[i-1] == question[j-1]:
                dp[i][j] = np.maximum(dp[i][j],dp[i+1][j+1]+1)
        if dp[i][1] == ansvalue:
            l = i -1
            break
    # TODO 如果最长公共子序列在question中的起始下标为0,则取最长公共子序列在content中最后一个位置到后面第一个标点符号(或空格)为止为答案
    # TODO 如果不为0,则取最长公共子序列在content中第一个位置往前的标点符号(或空格)为止的为答案
    # TODO 加分词结果
    answer_content = content[l:r+1]
    # print('answer_content...',answer_content,l,r)

    if answer_content in question or answer_content.replace('，','') in question:
        index = max(question.find(answer_content),question.find(answer_content.replace('，','')))


        if index == 0:

            content = content[r+1:content_len]
            i = len(content)
            comma_index = content.find('，',1)
            period_index = content.find('。',1)
            space_index = content.find(' ',1)

            if period_index != -1:
                i = min(period_index,i)
            elif comma_index != -1:
                i = min(comma_index, i)
            else:

                if space_index != -1:
                    i = min(space_index,i)
                space_index = content.find('　',1)
                if space_index != -1:
                    i = min(space_index,i)
            return content[0:i].replace('"','\"').replace("'", "\'")
        else:
            content = content[0:l]
            i = 0
            content_len = len(content)
            comma_index = last_index(content[:content_len-1],'，')
            period_index = last_index(content[:content_len-1],'。')
            space_index = last_index(content[:content_len-1],' ')
            i = max(comma_index,period_index,space_index,i)
            space_index = last_index(content[:content_len-1],'　')
            i = max(space_index,i)
            i = int(i)
            return content[i+1:len(content)].replace('"','\"').replace("'", "\'")

    answer_content_len = len(answer_content)
    current = ''
    while answer_content_len != 0:
        current = maxSubstring(answer_content,question)
        answer_content_len = len(current)
        if answer_content_len < 2:
            break
        answer_content= answer_content.replace(current,'')
        question = question.replace(current,'')


    return answer_content.replace('"','\"').replace("'", "\'")

    # for i in range(len(answer_content)):
    #     if answer_content[i] not in question:
    #         list.append(answer_content[i])
    # print('answer......',''.join(list))







def test(type=None):
    model_path = './data/model_db/content_3-tfidf-ngram=2-hashsize=8388608.npz'
    db_path = './data/model_db/content_3.db'
    ranker = TfidfDocRanker(tfidf_path=model_path, db_path=db_path)
    with open(os.path.join('data', type, 'data.txt'), 'r') as questions,\
        open(os.path.join('data', type, 'answers.txt'), 'w') as answers:
        question = True
        while question:
            question = questions.readline().strip()
            questions.readline()
            questions.readline()
            if question.find('Q:') == 0:
                try:

                    # print(question)
                    docs, _ = ranker.top_k_docs(question.replace('Q:','').strip(), 5)
                    ans_list = []
                    cand_score = 0
                    for text in docs:
                        text_list = re.split('[！？。!?]', text.strip())
                        sent_score = 0
                        for sent in text_list:
                            score = ranker.getSim(question, sent)
                            if score > sent_score:
                                sent_score = score
                        if sent_score > cand_score:
                            cand_score = sent_score
                            ans_list = text_list


                            # print(text[:50]+'....\t',str(doc_scores[i])+'\n')
                            # print(text+'\t',str(doc_scores[i])+'\n')
                    # print('候选句:\n')
                    #
                    # print(ans_list, '\t' + str(cand_score))

                    # print('答案：\n')
                    answers.write(LCS_Answer('。'.join(ans_list)+'。', question)[:35]+'\n')
                except RuntimeError:
                    answers.write(' \n')

                    print('RuntimeError')


def interactive( model, db_path):


    ranker = TfidfDocRanker(tfidf_path=model, db_path=db_path)
    # indx = ['1','2','3','4','5']
    while True:
        query = input('输入问题:\n')
        if query == 'exit' :
            exit(0)
        # if query in indx:
        #     print(docs[indx.index(query)])
        #     continue
        docs, doc_scores = ranker.top_k_docs(query, 5)



        print('\ntop_5_articles:\n')
        for i,text in enumerate(docs):
            print(text + '\t', str(doc_scores[i]) + '\n')

        ans_list = []
        cand_score = 0
        for text in docs:
            text_list = re.split('[！？。!?]', text.strip())
            sent_score = 0
            for sent in text_list:
                score = ranker.getSim(query, sent)
                if score > sent_score:
                    sent_score = score
            if sent_score > cand_score:
                cand_score = sent_score
                ans_list = text_list


            #print(text[:50]+'....\t',str(doc_scores[i])+'\n')
            # print(text+'\t',str(doc_scores[i])+'\n')
        print('候选句:\n')

        print(ans_list, '\t'+str(cand_score))


        print('答案：\n')
        print(LCS_Answer('。'.join(ans_list), query))


def retriever(model,db_path):
    ranker = TfidfDocRanker(tfidf_path=model, db_path=db_path)
    # indx = ['1','2','3','4','5']
    while True:
        query = input('输入问题:\n')
        if query == 'exit':
            exit(0)
        # if query in indx:
        #     print(docs[indx.index(query)])
        #     continue
        docs, doc_scores = ranker.top_k_docs_artid(query, 5)

        print('\ntop_5_articles:\n')
        for i, text in enumerate(docs):
            print(text[0] ,text[1],  '\t'+str(doc_scores[i]) + '\n')

        # ans_list = []
        # cand_score = 0
        # for text in docs:
        #     text_list = re.split('[！？。!?]', text.strip())
        #     sent_score = 0
        #     for sent in text_list:
        #         score = ranker.getSim(query, sent)
        #         if score > sent_score:
        #             sent_score = score
        #     if sent_score > cand_score:
        #         cand_score = sent_score
        #         ans_list = text_list
        #
        #
        #         # print(text[:50]+'....\t',str(doc_scores[i])+'\n')
        #         # print(text+'\t',str(doc_scores[i])+'\n')
        # print('候选句:\n')
        #
        # print(ans_list, '\t' + str(cand_score))
        #
        # print('答案：\n')
        # print(LCS_Answer('。'.join(ans_list), query))


if __name__ == '__main__':

    # warnings.filterwarnings('ignore')
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--model', type=str, default=None)
    # parser.add_argument('--db_path',type=str, default=None)
    # args = parser.parse_args()
    # retriever(args.model,args.db_path)

    process = Process()
    print(process.get_answer("外联网概念的确是未来互联网的一个重要发展方向","什么是未来互联网的一个重要发展方向？"))

    # test
    # parser = argparse.ArgumentParser()
    # parser.add_argument('type', type=str, default=None,
    #                     help='The question type')
    #
    # args = parser.parse_args()
    # test(args.type)




    # warnings.filterwarnings('ignore')
    # parser = argparse.ArgumentParser()
    # parser.add_argument('query', type=str, default=None,
    #                     help='The question')
    # parser.add_argument('--model', type=str, default=None)
    # parser.add_argument('--db_path',type=str, default=None)
    #
    #
    # args = parser.parse_args()
    # args.model = './data/content_3-tfidf-ngram=2-hashsize=8388608.npz'
    # args.db_path = './data/content_3.db'

        # for i in range(len(docs)):
        #     sentence, score = MaxSimSentence(docs[i], query).getSentence()
        #     print('\n\n'.join(sentence),str(score)+'\n')

