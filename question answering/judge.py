# -*- coding: utf-8 -*-
"""
计算预测的精确度
Created on Sat Dec 16 16:35:49 2017

@author: dmyan
"""
import sys

def readanswer():
    with open("./data/test.txt", "r+", encoding="utf-8") as f:
        with open('out.txt', 'w+', encoding="utf-8") as f1:
            for i in range(2040):
                for j in range(6):
                    line = f.readline().strip()
                    if line[0:1] == 'R' or line[0:1] == 'r':
                        f1.write(str(j-2)+"\n")


def test():
    """

    :return:
    """
    sum = 0
    readanswer()
    with open("out.txt", 'r') as f1:
        with open("pre_answer.txt", 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
    # print(lines1)
    # print(lines2)
    for i in range(len(lines1)):
        if lines1[i] == lines2[i]:
            sum += 1

    print('Accuracy:%.2f%%' % ((sum/len(lines1))*100))


if __name__ == '__main__':
    test()




