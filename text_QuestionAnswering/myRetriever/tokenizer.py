# -*- coding: utf-8 -*-
"""
Created on 18-10-15 上午11:54

@author: dmyan
"""
import regex
import logging
import jieba
logger = logging.getLogger(__name__)

class Tokenizer(object):
    """Base tokenizer class.
    Tokenizers implement tokenize, which should return a Tokens class.
    """
    def tokenize(self, text):
        raise NotImplementedError

    def shutdown(self):
        pass

    def __del__(self):
        self.shutdown()


class Tokenizer_jieba(Tokenizer):
    def __init__(self):
        jieba.setLogLevel(logging.INFO)
        self.words = ''
    def ngrams(self, n=1, as_strings=True):
        ngrams = [(s, e+1)
                  for s in range(len(self.words))
                  for e in range(s,min(s+n,len(self.words)))]
        if as_strings:
            ngrams = ['{}'.format(''.join(self.words[s:e])) for (s, e) in ngrams]
        return ngrams
    def init_words(self,text):
        pattern = regex.compile(r'[\p{P}]', flags=regex.MULTILINE)
        text = regex.sub(pattern,' ',text).replace('　', '')
        self.words = ' '.join(jieba.cut(text)).split()
if __name__ == '__main__':
    words = "新加坡总理妄称南海仲裁强而有力 外交部回应，，，，，。答：关于南海仲裁案仲裁庭作出的所谓裁决，中方已表明严正立场。有关裁决非法、无效，没有约束力。在刚刚结束的东亚合作系列外长会上，东盟方已明确表示作为整体对所谓仲裁案不持立场。"
    tokenier = Tokenizer_jieba()
    tokenier.init_words(words)
    print(tokenier.ngrams())