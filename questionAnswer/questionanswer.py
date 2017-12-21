import jieba.analyse
from gensim import corpora, models, similarities
import re
import numpy as np


def readanswer():
    """
    读取答案序列
    :return:
    """
    with open("./data/test.txt", "r+", encoding="utf-8") as f:
        with open('test_answer.txt', 'w+', encoding="utf-8") as f1:
            for i in range(2040):
                for j in range(6):
                    line = f.readline().strip()
                    if line[0:1] == 'R' or line[0:1] == 'r':
                        f1.write(str(j-2)+"\n")


def test():
    """
    测试预测结果
    :return:
    """
    readanswer()
    sum = 0
    with open("test_answer.txt", 'r') as f1:
        with open("pre_answer.txt", 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
    for i in range(len(lines1)):
        if lines1[i] == lines2[i]:
            sum += 1
    #print('Correct: %d total: %d' % (sum, len(lines1)))
    print('Accuracy:%.2f%%' % ((sum/len(lines1))*100))


def cal_sim():
    """
    计算相似度
    :return:
    """
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    documents = []  # 全部背景知识文本
    with open('./data/knowledge.txt', 'r+', encoding='utf-8') as f:
        for line in f:
            seg = jieba.cut(line, cut_all=False)
            seg_str = ' '.join(seg)
            word_list = seg_str.split()
            documents.append(word_list)
    with open('./data/train.txt', 'r+', encoding='utf-8') as f:
        file_lines = 61200
        sum_iter = int(file_lines / 6)
        for i in range(sum_iter):
            queryStr = []
            strR = ''
            for j in range(6):
                line = f.readline().strip()

                if line[0:1] == 'B' or line[0:1] == 'b':
                    queryStr.append(re.sub(r'[A-Z:]', ' ', line))
                elif line[0:1] == 'Q' or line[0:1] == 'q':
                    queryStr.append(re.sub(r'[A-Z:]', ' ', line))
                elif line[0:1] == 'R' or line[0:1] == 'r':
                    strR = re.sub(r'[A-Z:]', ' ', line)
            seg = jieba.cut(queryStr[0] +' '+ queryStr[1]+' '+strR, cut_all=False)
            seg_str = ' '.join(seg)
            word_list = seg_str.split()
            documents.append(word_list)
    # print(documents[0])

    dic = corpora.Dictionary(documents)
    # print(dic.token2id)
    corpus = [dic.doc2bow(document) for document in documents]  # 每个句子中的每个词对应的词频数
    # print(corpus)
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]  # 每个句子中的每个词对应的tfidf
    lsi = models.LsiModel(corpus_tfidf, id2word=dic, num_topics=1000)
    corpus_lsi = lsi[corpus_tfidf]
    index = similarities.MatrixSimilarity(lsi[corpus])

    return index, dic, documents, lsi


if __name__ == "__main__":
    top_k = 4
    np.seterr(divide='ignore', invalid='ignore')
    index, dic, documents, lsi = cal_sim()
    question = []  # 全部查询题目每一行[B+Q]
    answer = [] # 每一行对应一个题目的四个选项[A1,A2,A3,A4]
    r = 0
    w = 0

    with open('./data/test.txt', 'r+', encoding='utf-8') as f:
        file_lines = 12240
        sum_iter = int(file_lines / 6)
        for i in range(sum_iter):
            queryStr = []
            # strR = ''
            # strW = []
            ans = []
            for j in range(6):
                line = f.readline().strip()
                if line[0:1] == 'B' or line[0:1] == 'b':
                    queryStr.append(re.sub(r'[A-Z:]', '', line))
                elif line[0:1] == 'Q' or line[0:1] == 'q':
                    queryStr.append(re.sub(r'[A-Z:]', '', line))
                elif line[0:1] == 'R' or line[0:1] == 'r':
                    ans.append(re.sub(r'[A-Z:]', '', line))
                elif line[0:1] == 'W' or line[0:1] == 'w':
                    ans.append(re.sub(r'[A-Z:]', '', line))

            question.append(queryStr[0] + queryStr[1])
            answer.append(ans)
            # tmp[0] = queryStr[0] + queryStr[1]
            # tmp[1] = strR
            # for k, value in enumerate(strW):
            #     tmp[k + 2] = value
            # query.append(tmp)
    # print(np.shape(query)[0])
    n = np.shape(question)[0]
    correct = 0

    know_doc = []

    with open("pre_answer.txt", "w+") as f:
        for i in range(n):
            count = [-1] * 4
            query_sentence = question[i]
            seg = jieba.cut(query_sentence, cut_all=False)
            seg_str = ' '.join(seg)
            query_bow = dic.doc2bow(seg_str.split())
            query_lsi = lsi[query_bow]
            sims = index[query_lsi]
            sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
            result_k = sort_sims[0:top_k]
            know = []
            for k in range(len(result_k)):
                know.append(documents[int(result_k[k][0])])
            # print(know)
            # j计算候选知识和选项之间的相似度
            know_dic = corpora.Dictionary(know)
            # print(dic.token2id)
            know_corpus = [know_dic.doc2bow(document) for document in know]  # 每个句子中的每个词对应的词频数
            # print(corpus)
            know_tfidf = models.TfidfModel(know_corpus)
            know_corpus_tfidf = know_tfidf[know_corpus]  # 每个句子中的每个词对应的tfidf
            know_lsi = models.LsiModel(know_corpus_tfidf, id2word=know_dic, num_topics=20)
            corpus_lsi = know_lsi[know_corpus_tfidf]
            know_index = similarities.MatrixSimilarity(know_lsi[know_corpus])

            for j in range(4):
                ans = answer[i][j]
                ans_seg = jieba.cut(ans, cut_all=False)
                ans_seg_str = ' '.join(ans_seg)
                ans_query_bow = know_dic.doc2bow(ans_seg_str.split())
                ans_query_lsi = know_lsi[ans_query_bow]
                ans_sims = know_index[ans_query_lsi]
                ans_sort_sims = sorted(enumerate(ans_sims), key=lambda item: -item[1])
                ans_result = ans_sort_sims[0:5]
                count[j] = ans_result[0][1]
            f.write(str(np.argmax(count))+'\n')
    test()

    # for j in range(4):
    #     for k in range(len(know)):
    #         tmp = Levenshtein.distance(answer[i][j], ''.join(know[k]))
    #         if count[j] > tmp:
    #             count[j] = tmp
    # #print(count)
    # f.write(str(np.argmin(count)) + "\n")
    # print("Correct:%d Total:%d Accuracy:%.2f%%" % (correct, n, (correct/n)*100))
    # query_sentence = 'a' # query[1249][0]
    # while query_sentence:
    #     query_sentence = input('输入句子:')
    #     seg = jieba.cut(query_sentence, cut_all=False)
    #     seg_str = ' '.join(seg)
    #     query_bow = dic.doc2bow(seg_str.split())
    #     query_lsi = lsi[query_bow]
    #     sims = index[query_lsi]
    #     sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    #     result_k = sort_sims[0:top_k]
    #     know = []
    #     # print(sort_sims[0:top_k])
    #     print('query', query_sentence)
    #     for i in range(len(result_k)):
    #         know.append(documents[int(result_k[i][0])])
    #     for i in range(len(know)):
    #         print('know', know[i])
