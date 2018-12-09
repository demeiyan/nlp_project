# -*- coding: utf-8 -*-
"""
Created on 18-10-15 上午11:22

@author: dmyan
"""
import numpy as np
import scipy.sparse as sp
import argparse
import os
import math
import logging

from multiprocessing import Pool as ProcessPool
import multiprocessing
from multiprocessing.util import Finalize
from functools import partial
from collections import Counter
from doc_db import DocDB
from tokenizer import Tokenizer_jieba
from sklearn.utils import murmurhash3_32
from utils import save_sparse_csr

DOC2IDX = None
PROCESS_TOK = None
PROCESS_DB = None

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)

def init(tokenizer_class, db_class, db_opts):
    global PROCESS_TOK, PROCESS_DB
    PROCESS_TOK = tokenizer_class()
    Finalize(PROCESS_TOK, PROCESS_TOK.shutdown, exitpriority=100)
    PROCESS_DB = db_class(**db_opts)
    Finalize(PROCESS_DB, PROCESS_DB.close, exitpriority=100)

def fetch_text(doc_id):
    global PROCESS_DB
    return PROCESS_DB.get_doc_text(doc_id)

def getNgrams(text,ngram):
    global PROCESS_TOK
    PROCESS_TOK.init_words(text)
    return PROCESS_TOK.ngrams(ngram)

def hash(token, num_buckets):
    """Unsigned 32 bit murmurhash for feature hashing."""
    return murmurhash3_32(token, positive=True) % num_buckets


def count(ngram, hash_size, doc_id):
    global DOC2IDX
    row, col, data = [], [], []
    ngrams = getNgrams(fetch_text(doc_id),ngram)

    counts = Counter([hash(gram, hash_size) for gram in ngrams]) # {key:counts,...}

    row.extend(counts.keys()) # [key1, key2, key3...]
    col.extend([DOC2IDX[doc_id]] * len(counts))  # 文档号
    data.extend(counts.values()) # 词出现的次数

    # 最后返回矩阵形式 row表明哪几行有词，col表明哪一个文档中的词，data中的值表示一个词(ngram)出现了多少次
    return row, col, data


def get_count_matrix(args, db_opts):
    global DOC2IDX
    db_class = DocDB
    with db_class(**db_opts) as doc_db:
        doc_ids = doc_db.get_doc_ids()
    DOC2IDX = {doc_id: i for i, doc_id in enumerate(doc_ids)}

    # Setup worker pool
    tok_class = Tokenizer_jieba
    workers = ProcessPool(
        args.num_workers,
        initializer=init,
        initargs=(tok_class, db_class, db_opts)
    )

    # Compute the count matrix in steps (to keep in memory)
    logger.info('Mapping...')
    row, col, data = [], [], []
    step = max(int(len(doc_ids) / 10), 1)
    batches = [doc_ids[i:i + step] for i in range(0, len(doc_ids), step)]
    _count = partial(count, args.ngram, args.hash_size) # 绑定部分参数
    for i, batch in enumerate(batches):
        logger.info('-' * 25 + 'Batch %d/%d' % (i + 1, len(batches)) + '-' * 25)
        for b_row, b_col, b_data in workers.imap_unordered(_count, batch):
            row.extend(b_row)
            col.extend(b_col)
            data.extend(b_data)
    workers.close()
    workers.join()

    logger.info('Creating sparse matrix...')
    print('shape....', len(row), len(col), len(data))
    count_matrix = sp.csr_matrix(
        (data, (row, col)), shape=(args.hash_size, len(doc_ids))
    )
    count_matrix.sum_duplicates()
    return count_matrix, (DOC2IDX, doc_ids)

def get_tfidf_vectors(matrix):
    """
    tfidf = log(tf+1)*log((N - Nt + 0.5)/(Nt + 0.5))
    tf term frequency in document
    N number of doc
    Nt doc_freqs
    :param matrix:
    :return:
    """
    Nt = get_doc_freqs(matrix)
    N = matrix.shape[1]
    idf = np.log((N - Nt + 0.5)/(Nt + 0.5))
    tf = matrix.log1p()
    idf[idf<0] = 0
    idf = sp.diags(idf,0)
    tfidf = idf.dot(tf)
    return tfidf

def get_doc_freqs(matrix):
    """
    统计每行大于0的列数，也就是每个ngram的文档频率
    :param matrix:
    :return:
    """
    binary = (matrix>0).astype(int)
    doc_freqs = np.array(binary.sum(1)).squeeze()
    return doc_freqs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('db_path', type=str, default=None,
                        help='Path to sqlite db holding document texts')
    parser.add_argument('out_dir', type=str, default=None,
                        help='Directory for saving output files')
    parser.add_argument('--ngram', type=int, default=2,
                        help=('Use up to N-size n-grams '
                              '(e.g. 2 = unigrams + bigrams)'))
    parser.add_argument('--hash-size', type=int, default=int(math.pow(2, 23)),
                        help='Number of buckets to use for hashing ngrams')
    parser.add_argument('--num-workers', type=int, default=None,
                        help='Number of CPU processes (for tokenizing, etc)')
    args = parser.parse_args()
    if args.num_workers == None:
        args.num_workers = multiprocessing.cpu_count() - 1 or 1
    logging.info('Counting words...')
    count_matrix, doc_dict = get_count_matrix(args,{'db_path':args.db_path})


    logging.info('generating tfidf vectors...')
    tfidf = get_tfidf_vectors(count_matrix)

    doc_freqs = get_doc_freqs(count_matrix)

    basename = os.path.splitext(os.path.basename(args.db_path))[0]

    basename += ('-tfidf-ngram=%d-hashsize=%d'%(args.ngram,args.hash_size))
    filename = os.path.join(args.out_dir,basename)

    logging.info('saving...')

    metadata ={
        'doc_freqs':doc_freqs,
        'hash_size':args.hash_size,
        'ngram':args.ngram,
        'doc_dict':doc_dict
    }
    save_sparse_csr(filename, tfidf, metadata)