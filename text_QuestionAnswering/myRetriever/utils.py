# -*- coding: utf-8 -*-
"""
Created on 18-10-15 上午11:22

@author: dmyan
"""
import numpy as np
import scipy.sparse as sp
import unicodedata

# ------------------------------------------------------------------------------
# Sparse matrix saving/loading helpers.
# ------------------------------------------------------------------------------

DEFAULTS = {
    'db_path': 'data/content.db',
    'tfidf_path':
        'data/content-tfidf-ngram=2-hashsize=8388608.npz',
}
def save_sparse_csr(filename, matrix, metadata=None):
    data = {
        'data': matrix.data,
        'indices': matrix.indices,
        'indptr': matrix.indptr,
        'shape': matrix.shape,
        'metadata': metadata,
    }
    np.savez(filename, **data)


def load_sparse_csr(filename):
    loader = np.load(filename)
    matrix = sp.csr_matrix((loader['data'], loader['indices'],
                            loader['indptr']), shape=loader['shape'])
    return matrix, loader['metadata'].item(0) if 'metadata' in loader else None

def normalize(text):
    """Resolve different type of unicode encodings."""
    return unicodedata.normalize('NFD', text)
