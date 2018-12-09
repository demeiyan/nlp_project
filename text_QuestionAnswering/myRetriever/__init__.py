# -*- coding: utf-8 -*-
"""
Created on 18-10-15 上午11:11

@author: dmyan
"""
DEFAULTS = {
    'db_path': 'data/content.db',
    'tfidf_path':
        'data/docs-tfidf-ngram=2-hash=16777216-tokenizer=simple.npz',
}


def set_default(key, value):
    global DEFAULTS
    DEFAULTS[key] = value


if __name__ == '__main__':
    pass