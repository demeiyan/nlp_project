# -*- coding: utf-8 -*-
"""
Created on 18-10-17 下午8:38

@author: dmyan
"""

import logging
import utils as util
from tokenizer import Tokenizer_jieba
from sklearn.utils import murmurhash3_32
import scipy.sparse as sp
import numpy as np
logger = logging.getLogger('__name__')
from doc_db import DocDB
import argparse
DEFAULTS = {
    'db_path': 'data/content.db',
    'tfidf_path':
        'data/content-tfidf-ngram=2-hashsize=8388608.npz',
}

class TfidfDocRanker(object):
    def __init__(self, tfidf_path=None, db_path=None):
        self.tfidf_path = tfidf_path or DEFAULTS['tfidf_path']
        self.db_path = db_path or DEFAULTS['db_path']
        logger.info('load tfidf file...')
        matrix,metadata = util.load_sparse_csr(self.tfidf_path)
        self.doc_mat = matrix
        self.hash_size = metadata['hash_size']
        self.doc_freqs = metadata['doc_freqs']
        self.ngram = metadata['ngram']
        self.doc_dict = metadata['doc_dict']
        self.num_docs = len(self.doc_dict[0])

    def getNgrams(self,text):
        tokenizer = Tokenizer_jieba()
        tokenizer.init_words(text)
        return tokenizer.ngrams(self.ngram)

    def hash(self, token, num_buckets):
        """Unsigned 32 bit murmurhash for feature hashing."""
        return murmurhash3_32(token, positive=True) % num_buckets
    def text2spvector(self, query):
        """
        返回query的稀疏tfidf向量
        tfidf = log(tf+1)*log((N-nt+0.5)/(nt+0.5))
        :param query:
        :return:
        """
        ngrams = self.getNgrams(query)
        hash_query = [self.hash(gram, self.hash_size) for gram in ngrams]
        if len(hash_query) == 0:
            raise RuntimeError('No valid word in: %s'%query)
        q_unique, q_counts = np.unique(hash_query, return_counts=True) # 返回句子中词的key和counts
        tf = np.log1p(q_counts)

        Nt = self.doc_freqs[q_unique]
        N = self.num_docs
        idf = np.log((N - Nt + 0.5)/(Nt + 0.5))
        idf[idf<0] = 0

        tfidf = np.multiply(tf,idf)
        indptr = np.array([0, len(q_unique)])
        spvector = sp.csr_matrix(
            (tfidf, q_unique, indptr),shape=(1, self.hash_size)
        )
        return spvector

    def getSim(self, query, candidate):
        # TODO 加入共有词的index差值
        q_vector = self.text2spvector(query)
        cand_vector = self.text2spvector(candidate).transpose()


        # print(q_vector.data)
        q_min = q_vector.min()
        q_max = q_vector.max()

        cand_min = cand_vector.min()
        cand_max = cand_vector.max()

        q_vector.data = (q_vector.data - q_min)/(q_max - q_min)
        cand_vector.data = (cand_vector.data - cand_min)/(cand_max - cand_min)
        # print(q_vector.data, cand_vector.data)
        res = q_vector*cand_vector
        if res.data:
            return res.data[0]
        else:
            return 0.0
        # print('res.data....', res.data)
        # return res.data[0]
        # print(res.data)

    def get_docs(self,id):
        doc_db = DocDB(self.db_path)
        doc_id = self.doc_dict[1][id]
        return doc_db.get_doc_text(doc_id)

    def get_docs_artid(self, id):
        doc_db = DocDB(self.db_path)
        doc_id = self.doc_dict[1][id]
        return doc_db.get_text_artid(doc_id)

    def top_k_docs(self, query, k=1):

        spvector = self.text2spvector(query)

        res = spvector*self.doc_mat # (data,indices,indptr)

        if len(res.data)<=k:
            idx = np.argsort(-res.data)
        else:
            k_idx = np.argpartition(-res.data, k)[0:k]
            idx = k_idx[np.argsort(-res.data[k_idx])]
        doc_scores = res.data[idx]
        docs = [self.get_docs(id) for id in res.indices[idx]]
        return docs, doc_scores

    def top_k_docs_artid(self, query, k=1):
        spvector = self.text2spvector(query)

        res = spvector*self.doc_mat # (data,indices,indptr)

        if len(res.data)<=k:
            idx = np.argsort(-res.data)
        else:
            k_idx = np.argpartition(-res.data, k)[0:k]
            idx = k_idx[np.argsort(-res.data[k_idx])]
        doc_scores = res.data[idx]
        docs = [self.get_docs_artid(id) for id in res.indices[idx]]
        return docs, doc_scores


if __name__ == '__main__':



    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default=None)
    parser.add_argument('--db_path',type=str, default=None)
    args = parser.parse_args()

    logger.info('Initializing ranker...')
    if args.model == None:
        args.model = DEFAULTS['tfidf_path']
    ranker = TfidfDocRanker(tfidf_path=args.model, db_path=args.db_path)
    query = '世界最大的石油出口国是哪个？'
    # candicate = '沙特是世界最大的石油出口出口国'
    # candicate = '随着世界世界性能源紧缺导致的石油、天然天然气等能源价格能源价格的飞涨，世界最大天然天然气出口出口国和第二大石油出口出口国罗斯俄罗斯逐步走出经济低谷自2000年开始走出危机后，罗斯俄罗斯年均经济增长增长率超过6%'
    #
    # print(ranker.getSim(query,candicate))
    candicate = '作为继承了冷战阵营一方主帅苏联绝大多数力量的俄罗斯，也从未放弃其强国的意识'
    print(ranker.getSim(query, candicate))
    # while True:
    #     query = input('输入问题:\n')
    #     if query == 'exit' :
    #         exit(0)
    #     docs, doc_scores = ranker.top_k_docs(query, 5)
    #     for i, text in enumerate(docs):
    #         # print(text[:50]+'....\t',str(doc_scores[i])+'\n')
    #         print(text+'\t',str(doc_scores[i])+'\n')