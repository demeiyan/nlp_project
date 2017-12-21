from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
import numpy as np
import collections
import re
def loady(filename):
    with open(filename, 'r+') as f:
        y_train = f.read().split('\n')
        while '' in y_train:
            y_train.remove('')
        y_train = [int(i) for i in y_train]
    return np.array(y_train)


if __name__ == '__main__':

    batch = 32
    top_words = 16442
    max_review_length = 50
    EMBEDDING_SIZE = 128
    HIDDEN_LAYER_SIZE = 64

    #训练集
    x_train = []
    word_freqs = collections.Counter()
    with open('dataset/train_x.txt', "r+") as f:
        for line in f.readlines():
            list = line.strip().split()#re.split('\\s+', line.strip().strip('\n').lower())
            while '' in list:
                list.remove('')
            for word in list:
                 if re.search(r'\d+',word) != None:
                     list.remove(word)
            for index in list:
                word_freqs[index] += 1
    wordtoIndex = {x[0]: i + 2 for i, x in enumerate(word_freqs.most_common(top_words))}  # 提取共现次数最高的top_words个单词
    wordtoIndex['oov'] = 1
    wordtoIndex['pad'] = 0
    with open('dataset/train_x.txt', "r+") as f:
        for line in f.readlines():
            list = line.strip().split()#re.split('\\s+', line.strip().strip('\n').lower())
            while '' in list:
                list.remove('')
            sentence = []
            for word in list:
                if word in wordtoIndex:
                    sentence.append(wordtoIndex[word])
                else:
                    sentence.append(wordtoIndex['oov'])
            x_train.append(sentence)
    x_train = sequence.pad_sequences(x_train, maxlen=max_review_length)

    # 验证集
    x_dev = []
    with open('dataset/dev_x.txt', 'r+') as f:
        for line in f.readlines():
            list = line.strip().split()#re.split('\\s+', line.strip().strip('\n').lower())
            sentence = []
            for word in list:
                if word in wordtoIndex:
                    sentence.append(wordtoIndex[word])
                else:
                    sentence.append(wordtoIndex['oov'])
            x_dev.append(sentence)
    x_dev = sequence.pad_sequences(x_dev, maxlen=max_review_length)

    #测试集
    x_test = []
    with open('dataset/test_x.txt', 'r+') as f:
        for line in f.readlines():
            list = line.strip().split()#re.split('\\s+', line.strip().strip('\n').lower())
            sentence = []
            for word in list:
                if word in wordtoIndex:
                    sentence.append(wordtoIndex[word])
                else:
                    sentence.append(wordtoIndex['oov'])
            x_test.append(sentence)
    x_test = sequence.pad_sequences(x_test, maxlen=max_review_length)


    y_train = loady('dataset/train_y.txt')
    y_train = [i-1 for i in y_train]
    y_train = np_utils.to_categorical(y_train, num_classes=5)
    y_dev = loady('dataset/dev_y.txt')
    y_dev = [i-1 for i in y_dev]
    y_dev = np_utils.to_categorical(y_dev, num_classes=5)

    x_com = np.row_stack((x_train, x_dev))
    y_com = np.row_stack((y_train, y_dev))
    #训练
    Xtrain, Xtest, ytrain, ytest = train_test_split(x_com, y_com, test_size=0.2, random_state=42)
    model = Sequential()
    model.add(Embedding(input_dim=top_words, output_dim=EMBEDDING_SIZE, input_length=max_review_length))
    model.add(Dropout(0.3))
    model.add(LSTM(HIDDEN_LAYER_SIZE, dropout=0.3, recurrent_dropout=0.3))
    model.add(Dropout(0.3))
    model.add(Dense(5))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    model.fit(Xtrain, ytrain, batch_size=batch, epochs=3, validation_data=(Xtest, ytest))
    #model.fit(x_train, y_train, batch_size=batch, epochs=2, validation_data=(x_dev, y_dev))
    scores = model.evaluate(x_dev, y_dev, verbose=2)
    print("Accuracy: %.2f%%" % (scores[1] * 100))
    y_test_tmp = model.predict(x_test, batch_size=batch)
    i = 0
    y_test = np.zeros(2211)
    for row in y_test_tmp:
        y_test[i] = np.argmax(row)+1
        i = i + 1
    with open('dataset/test_y.txt', 'w') as f:
        for label in y_test:
            f.write(str(int(label))+'\n')

