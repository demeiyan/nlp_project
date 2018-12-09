# -*- coding: utf-8 -*-
"""
Created on 18-9-4 上午8:56

@author: dmyan
"""
from __future__ import print_function
import json
import nltk
import os
from tqdm import tqdm
import sys
import jieba
from pyhanlp import *
import matplotlib.pyplot as plt
import numpy as np
import argparse


def data_from_json(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data

def read_related_question(dataset, tier, prefix):
    qn = 0
    title_questions = []
    with open(os.path.join(prefix, 'title.txt'), mode='r', encoding='utf8') as title:
        line = title.readline().strip('\r\n')

        while line:
            title_questions.append(line)
            line = title.readline().strip('\r\n')

    with open(os.path.join(prefix, tier + '.index_question'), 'w', encoding='utf8') as question_file, \
            open(os.path.join(prefix, tier + '.index_answer'), 'w', encoding='utf8') as answer_file:

        for articles_id in tqdm(range(len(dataset)), desc="Preprocessing {}".format(tier)):
            content = dataset[articles_id]['article_content'].strip()
            art_id = dataset[articles_id]['article_id'].strip()
            content = content.replace(' ', '').replace(' ', '').replace('　', '')
            content = content.replace("``", '" ').replace('\n', '').replace('\t', '')
            questions = dataset[articles_id]['questions']
            for qid in range(len(questions)):
                answer = questions[qid]['answer'].replace(' ', '').replace(' ', '').replace('　', '').replace("``", '" ').replace('\n', '').replace('\t', '')
                answer_start = content.find(answer)
                question = questions[qid]['question']
                if question in title_questions:
                    continue
                if answer_start != -1:
                    qn += 1
                    question_file.write(str(art_id)+'\t'+question.strip().replace('\t', '') + '\n')
                    answer_file.write(answer + '\n')
    return qn


def read_write_dataset(dataset, tier, prefix):
    qn,an = 0,0

    num_content_skipped = 0
    num_errors_parsing = 0
    title_questions = []
    with open(os.path.join(prefix, 'title.txt'), mode='r',encoding='utf8') as title:
        line = title.readline().strip('\r\n')

        while line:
            title_questions.append(line)
            line = title.readline().strip('\r\n')

    with open(os.path.join(prefix, tier+'.rawcontent'),  'w', encoding='utf8') as content_file, \
        open(os.path.join(prefix,tier+'.rawquestion'), 'w', encoding='utf8') as question_file, \
        open(os.path.join(prefix,tier+'.rawanswer'), 'w', encoding='utf8') as answer_file:

        for articles_id in tqdm(range(len(dataset)), desc="Preprocessing {}".format(tier)):
            content = dataset[articles_id]['article_content'].strip()
            art_id = dataset[articles_id]['article_id'].strip()
            content = content.replace(' ', '').replace(' ', '').replace('　', '')
            content = content.replace("``", '" ').replace('\n', '').replace('\t','')
            questions = dataset[articles_id]['questions']
            for qid in range(len(questions)):
                answer = questions[qid]['answer']
                answer_start = content.find(answer)
                question = questions[qid]['question']
                if question in title_questions:
                    continue
                if answer_start != -1:

                    qn += 1
                    content_file.write(content+'\n')
                    question_file.write(question+'\n')
                    answer_file.write(answer+'\n')
    return qn


def getType(data, type, path, count):
    cnt = 0
    data_list = []
    with open(os.path.join('data',path,'data.txt'), 'w') as w:
        for qid in range(len(data)):
            question = data[qid]
            if question['question_type'] == type:
                data_list.append(question)
        rand_idx = np.random.randint(len(data_list),size=count)

        for idx in rand_idx:
            question = data_list[idx]
            w.write('Q:'+question['question']+'\n'+'A:'+question['answer']+'\n\n')


def getSingleType(dataset, type):
    for articles_id in tqdm(range(len(dataset)), desc="Preprocessing "):
        questions =dataset[articles_id]['questions']
        for qid in range(len(questions)):
            if questions[qid]['question_type'] == type:
                print(questions[qid])



# def getType(data):
#     with open('data/list/'+'questions.txt','w') as w:
#         for qid in range(len(data)):
#             question = data[qid]
#             if question['question_type'] == '列表型问题':
#                 w.write(question['question']+'\t'+question['answer']+'\n')
#                 # print(question['question']+'\t',question['answer'])



if __name__ == '__main__':
    # 87257
    # data = data_from_json('data/question.json')
    # print(read_related_question(data,'train','data/rawtexts'))

    data = data_from_json('data/question.json')
    getSingleType(data,'篇章型问题')

    # getType(data)


    # parser = argparse.ArgumentParser()
    # parser.add_argument('type', type=str, default=None,
    #                     help='The question type')
    #
    # parser.add_argument('path', type=str, default=None,
    #                     help='result path')
    #
    # parser.add_argument('count', type=int, default=None,
    #                     help='count')
    # args = parser.parse_args()
    #
    #
    # data = data_from_json('data/text.json')
    # getType(data, args.type, args.path, args.count)






     #for i in range(len(content_segs)):
     # print(content_segs)
     # print(token_idx_map(content,content_segs))
     # print(content[309:330])
     # print(content.find("美国的F-35当中的F-35B型号"))




    # content_len = [0]*50
    # question_len = [0]*20
    # answer_len = [0]*20
    # cnt = [0]*3
    # num = 0
    # with open('./JS_data/question.json', 'r', encoding='utf8') as f:
    #     data = json.load(f)
    #     for i in range(len(data)):
    #
    #         content_segs = tokenize(data[i]['article_content'])
    #         # if len(content_segs) < 2500:
    #         #     content_len[int(len(content_segs)/50)] += 1
    #         if len(content_segs) <1000:
    #             cnt[0] += 1
    #             questions = data[i]['questions']
    #             for j in range(len(questions)):
    #                 question = questions[j]['question']
    #                 answer = questions[j]['answer']
    #                 question_segs = tokenize(question)
    #                 answer_segs = tokenize(answer)
    #                 num += 1
    #                 if len(question_segs) < 75:
    #                     cnt[1] += 1
    #                 if len(answer_segs) < 20:
    #                     cnt[2] += 1
    #                 # if len(question_segs) < 100:
    #                 #     question_len[int(len(question_segs)/5)] +=1
    #                 # if len(answer_segs) < 20 :
    #                 #     answer_len[len(answer_segs)] +=1
    # print(cnt,num)
    # x = np.arange(50)
    #
    #
    # plt.figure()
    # plt.plot(x, content_len,'o')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.savefig('./content.png')
    #
    # x = np.arange(20)
    #
    #
    # plt.figure()
    # plt.plot(x, question_len,'o')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.savefig('./question.png')
    #
    # x = np.arange(20)
    # plt.figure()
    # plt.plot(x, answer_len,'o')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.savefig('./answer.png')