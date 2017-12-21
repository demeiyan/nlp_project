# -*- coding: utf-8 -*-
"""
计算预测的精确度
Created on Sat Dec 16 16:35:49 2017

@author: dmyan
"""
sum = 0
with open("out.txt", 'r') as f1:
    with open("tmp.txt", 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
print(lines1)
print(lines2)
for i in range(len(lines1)):
    if lines1[i] == lines2[i]:
        sum += 1
print(sum)
print(sum/len(lines1))



