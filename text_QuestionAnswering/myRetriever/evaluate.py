# -*- coding: utf-8 -*-
"""
Created on 18-10-23 下午8:36

@author: dmyan
"""
from tfidf_doc_ranker import TfidfDocRanker
# from sentence_search.getMaxSimSentence import MaxSimSentence
import warnings
import argparse
import json

def doc_retriever():
    warnings.filterwarnings('ignore')
    ranker = TfidfDocRanker()
    # indx = ['1','2','3','4','5']
    cnt = [0]*5
    # query = '杀死“伊斯兰国”负责管理哪些等业务的高级头目萨耶夫'
    # docs, _ = ranker.top_k_docs(query, 5)
    with open('data/error.txt','w') as error,\
        open('data/train.rawcontent', 'r') as contents,\
         open('data/train.rawquestion', 'r') as questions:
        question = questions.readline().strip()
        while question:
            content = contents.readline().strip()
            docs, _ = ranker.top_k_docs(question, 5)
            for i in range(len(docs)):
                if content == docs[i]:
                    cnt[i] += 1
                    break
                if i == 4:
                    i += 1
            if i >= 5:
                error.write(question+'\n')
            question = questions.readline().strip()
    print(cnt)


# def search_sentence():
#     warnings.filterwarnings('ignore')
#     ranker = TfidfDocRanker()
#     # indx = ['1','2','3','4','5']
#     cnt = [0] * 3
#     # query = '杀死“伊斯兰国”负责管理哪些等业务的高级头目萨耶夫'
#     # docs, _ = ranker.top_k_docs(query, 5)
#     with open('data/train.rawquestion', 'r') as questions, \
#             open('data/train.rawanswer', 'r') as answers:
#         question = questions.readline().strip()
#         while question:
#             sre = 0
#             result_sen = []
#             answer = answers.readline().strip()
#             docs, _ = ranker.top_k_docs(question, 5)
#
#             for i in range(len(docs)):
#                 if len(docs[i].strip()) > 0:
#                     sentence, score = MaxSimSentence(docs[i], question).getSentence()
#                     if score > sre:
#                         result_sen = sentence
#             for i, sen in enumerate(result_sen):
#                 if answer in sen:
#                     cnt[i] += 1
#                     break
#             question = questions.readline().strip()
#     print(cnt)


def retrieve_data(model, db_path, size):
    # 87257
    # cnt = [0] * size
    # index = 0
    ranker = TfidfDocRanker(tfidf_path=model, db_path=db_path)
    q_words = []
    with open('./data/rawtexts/d_q_words.txt', mode='r', encoding='utf8') as qw:
        line = qw.readline().strip('\r\n')
        while line:
            q_words.append(line)
            line = qw.readline().strip('\r\n')
    q_words.sort(key=len, reverse=True)
    # print(q_words)
    cand_data = []
    with open('data/rawtexts/train.index_question', 'r') as questions, \
            open('data/rawtexts/train.index_answer', 'r') as answers:
        question = questions.readline().strip()
        while question:
            data = {}
            q_list = question.split('\t')
            answer = answers.readline().strip()
            art_id = q_list[0].strip()
            query = q_list[1].strip()
            data['question'] = query
            data['answer'] = answer
            for qw in q_words:
                if qw in query:
                    query = query.replace(qw, ' ')
                    break
            docs, _ = ranker.top_k_docs_artid(query, size)
            data['cand_sentence'] = docs
            cand_data.append(data)
            question = questions.readline().strip()
    with open('./data/cand50.json', mode='w', encoding='utf-8') as fp:
        json.dump(cand_data, fp, ensure_ascii=False)



def doc_3_retriever(model, db_path,size):
    # 87257
    cnt = [0]*size
    index = 0
    ranker = TfidfDocRanker(tfidf_path=model, db_path=db_path)
    q_words = []
    with open('./data/rawtexts/d_q_words.txt', mode='r',encoding='utf8') as qw:
        line = qw.readline().strip('\r\n')
        while line:
            q_words.append(line)
            line = qw.readline().strip('\r\n')
    q_words.sort(key=len, reverse=True)
    # print(q_words)

    with open('data/rawtexts/train.index_question','r') as questions,\
        open('data/error'+str(size)+'.txt', 'w') as errors,\
        open('data/rawtexts/train.index_answer', 'r') as answers:
        question = questions.readline().strip()
        while question:
            # print(question)
            q_list = question.split('\t')
            answer = answers.readline().strip()
            art_id = q_list[0].strip()
            query = q_list[1].strip()
            for qw in q_words:
                if qw in query:
                    query = query.replace(qw, ' ')
                    break
            docs, _ = ranker.top_k_docs_artid(query, size)
            index = 0
            for i, text in enumerate(docs):
                cand = text[0].strip()
                idx = text[1]
                # if art_id == str(idx).strip() or answer in cand:
                if answer in cand:
                    cnt[i] += 1
                    break
                index = i+1
            # print(cnt)
            if index >= size:
                errors.write(str(art_id)+'\t'+query+'\t'+answer+'\n')
            question = questions.readline().strip()
    print(cnt)



if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default=None, help="TFIDF模型文件")
    parser.add_argument('--db_path',type=str, default=None, help="原始文档存储位置")
    parser.add_argument('--size', type=int, default=None, help="返回的文档数目")
    args = parser.parse_args()
    retrieve_data(args.model, args.db_path, args.size)
    # doc_3_retriever(args.model,args.db_path,args.size)
