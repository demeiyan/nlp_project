# -*- coding: utf-8 -*-
"""
Created on 18-5-1 下午9:05

@author: dmyan
"""

import random
import numpy as np
def getRandomContext(C):
    tokens = ["a", "b", "c", "d", "e"]
    return tokens[random.randint(0, 4)], \
           [tokens[random.randint(0, 4)] for i in xrange(2 * C)]

if __name__ == '__main__':
    print random.randint(0, 4)
    print getRandomContext(5)
    print 5 +\
        5
    random.seed(31415)
    np.random.seed(9265)