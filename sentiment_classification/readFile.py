import collections
import re
import numpy as np
from keras.preprocessing import sequence
if __name__ == '__main__':
    # with open('dataset/train_y.txt', 'r+') as f:
    #     y_train = f.read().split('\n')
    #     while '' in y_train:
    #         y_train.remove('')
    #     y_train = [int(i) for i in y_train]
    top_words = 16652
    max_review_length = 50
    filename = 'dataset/train_x.txt'
    sample_num = 0
    x_train = []
    word_freqs = collections.Counter()
    with open(filename, "r+") as f:
        for line in f.readlines():
            #sample_num += 1
            list = line.strip().split()#re.split('\\s+', line.strip().strip('\n').lower())
            for word in list:
                  if re.search(r'\d+',word) != None:
                     list.remove(word)
                 #if re.search(r'[^a-zA-Z]',word) != None:
                     #list.remove(word)
            while '' in list:
                list.remove('')
            if sample_num < len(list):
                 sample_num = len(list)
            for index in list:
          
                 word_freqs[index] += 1
                 
    with open('dataset/dev_x.txt', "r+") as f:
        for line in f.readlines():
            #sample_num += 1
            list = line.strip().split()#re.split('\\s+', line.strip().strip('\n').lower())
            for word in list:
                  if re.search(r'\d+',word) != None:
                     list.remove(word)
                 #if re.search(r'[^a-zA-Z]',word) != None:
                     #list.remove(word)
            while '' in list:
                list.remove('')
            if sample_num < len(list):
                 sample_num = len(list)
            for index in list:
                 word_freqs[index] += 1
    with open('dataset/test_x.txt', "r+") as f:
        for line in f.readlines():
            #sample_num += 1
            list = line.strip().split()#re.split('\\s+', line.strip().strip('\n').lower())
            for word in list:
                  if re.search(r'\d+',word) != None:
                     list.remove(word)
                 #if re.search(r'[^a-zA-Z]',word) != None:
                     #list.remove(word)
            while '' in list:
                list.remove('')
            if sample_num < len(list):
                 sample_num = len(list)
            for index in list:
                 word_freqs[index] += 1
                
    wordtoIndex = {x[0]: i + 2 for i, x in enumerate(word_freqs.most_common(top_words))}  # 提取共现次数最高的top_words个单词
    wordtoIndex['oov'] = 1
    wordtoIndex['pad'] = 0
    with open(filename, "r+") as f:
        for line in f:
            list = line.strip().split()#re.split('\\s+', line.strip().strip('\n').lower())
            sentence = []
            for word in list:
                if word in wordtoIndex:
                    sentence.append(wordtoIndex[word])
                else:
                    sentence.append(wordtoIndex['oov'])
            x_train.append(sentence)
           
    x_train = np.array(x_train)
    x_train = sequence.pad_sequences(x_train,max_review_length)