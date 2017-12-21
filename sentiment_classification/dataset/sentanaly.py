#import nltk
import collections
import numpy as np
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
from keras.layers.core import Activation, Dense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.utils import np_utils
maxlen = 0  #句子最大长度
#word_freqs = collections.Counter()  #词频
word_freqs=collections.Counter()
line_lenth=collections.Counter()
num_recs = 0 # 样本数
num_valid = 0# 验证集
num_test = 0 #测试集
f=open('./train_x.txt','r+')
#f=open('./train_y.txt','r+')
linenum=0
i=0
for line in f.readlines():
    i=i+1
    words=line.strip().split()
    line_lenth[i]=len(words)
    if len(words) > maxlen:
        maxlen = len(words)
        linenum=i
    for word in words:
        
        word_freqs[word]=word_freqs[word]+1
        
    num_recs += 1
    #print(type(line))
f.close()   
print('max_len ',maxlen)
print('nb_words ', len(word_freqs))
print('line number',num_recs)
index=word_freqs.most_common()
#print(index)
linestatistic=line_lenth.most_common(30)
word2index = {x[0]: i+2 for i, x in enumerate(index)}
MAX_FEATURES = 16657
MAX_FEATURES = len (index)
MAX_SENTENCE_LENGTH = 50
vocab_size = min(MAX_FEATURES, len(index)) + 2
#word2index = {x[0]: i+2 for i, x in enumerate(word_freqs.most_common(MAX_FEATURES))}
word2index["PAD"] = 0
word2index["UNK"] = 1
index2word = {v:k for k, v in word2index.items()}

X = np.empty(num_recs,dtype=list)
y = np.zeros(num_recs)

with open('./test_x.txt','r+') as f:
    for line in f:
        num_test+=1
test_X = np.empty(num_test,dtype=list)
test_y = np.zeros(num_test)
i=0
with open('./test_x.txt','r+') as f:
    for line in f:
        words = line.strip().split()
        
        seqs = []
        for word in words:
            if word in word2index:
                seqs.append(word2index[word])
            else:
                seqs.append(word2index["UNK"])
        test_X[i] = seqs
        #sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)
        #y[i] = int(label)
        i += 1
test_X = sequence.pad_sequences(test_X, maxlen=MAX_SENTENCE_LENGTH)

with open('./dev_x.txt','r+') as f:
    for line in f:
        num_valid+=1
valid_X = np.empty(num_valid,dtype=list)
valid_y = np.zeros(num_valid)
#验证集X
i=0
with open('./dev_x.txt','r+') as f:
    for line in f:
        words = line.strip().split()
        
        seqs = []
        for word in words:
            if word in word2index:
                seqs.append(word2index[word])
            else:
                seqs.append(word2index["UNK"])
        valid_X[i] = seqs
        #sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)
        #y[i] = int(label)
        i += 1
valid_X = sequence.pad_sequences(valid_X, maxlen=MAX_SENTENCE_LENGTH)

#验证集y
i=0
with open('./dev_y.txt','r+') as f:
    for line in f:
        lable=int(line)
        valid_y[i]=lable-1
        i+=1
"""        if lable==3:
            valid_y[i]=1
        else:
            valid_y[i]=0"""
valid_y=np_utils.to_categorical(valid_y)        

#训练集x
i=0
with open('./train_x.txt','r+') as f:
    for line in f:
        words = line.strip().split()
        
        seqs = []
        for word in words:
            if word in word2index:
                seqs.append(word2index[word])
            else:
                seqs.append(word2index["UNK"])
        X[i] = seqs
        #sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)
        #y[i] = int(label)
        i += 1
X = sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)

#训练集y
i=0
with open('./train_y.txt','r+') as f:
    for line in f:
        lable=int(line)
        y[i]=lable-1
        i+=1
y=np_utils.to_categorical(y)
"""        if lable==3:
            y[i]=1
        else:
            y[i]=0
        i+=1"""
        #sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)
        #y[i] = int(label)
bigx=np.row_stack((X,valid_X))
bigy=np.row_stack((y, valid_y))
#Xtrain, Xtest, ytrain, ytest = bigx, valid_X, bigy, valid_y
Xtrain, Xtest, ytrain, ytest = train_test_split(bigx, bigy, test_size=0.2, random_state=42)
EMBEDDING_SIZE = 128
HIDDEN_LAYER_SIZE = 64

model = Sequential()
model.add(Embedding(vocab_size, EMBEDDING_SIZE,input_length=MAX_SENTENCE_LENGTH))
model.add(LSTM(HIDDEN_LAYER_SIZE, dropout=0.3, recurrent_dropout=0.3))
model.add(Dense(5))
model.add(Activation("softmax"))
model.compile(loss="categorical_crossentropy", optimizer="adam",metrics=["accuracy"])

BATCH_SIZE = 32
NUM_EPOCHS = 2
model.fit(Xtrain, ytrain, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS,validation_data=(Xtest, ytest))
#sample=np.array()

#sample.shape=(None,50)
predict=model.predict(test_X)
for i in range(num_test):
    test_y[i]=np.argmax(predict[i])+1
f=open('output.txt','w')
for i in range(num_test):
    f.write(str(int(test_y[i]))+'\n')
f.close()
##print(predict)