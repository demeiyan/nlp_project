# -*- coding: utf-8 -*-
"""
Created on 18-9-30 下午5:02

@author: dmyan
"""
from sentence_search.sentences import Sentence

from sentence_search.SentenceSimilarity import *


class MaxSimSentence(object):
    def __init__(self, content, question):

        self.sentence = Sentence(content)
        self.question = question


    def getSentence(self):
        ss = SentenceSimilarity(self.sentence.get_cuted_token_list())
        ss.TfidfModel()
        return ss.similarity(self.question)


if __name__ == '__main__':
    content = """
    据海军时报2010年6月26日报道海军型F-35闪电II型联合攻击战斗机在真实航母着舰应力状况下能否停住？这是该机于2010年6月6日在德克萨斯成功首飞后面临的又一重大问题。  洛马公司已经开始对飞机进行应力测试，包括将飞机从11英尺高的高度坠落，以测试飞机的结构强度。公司在各种角度和重量分布情况下进行了坠落试验，以模拟可能在舰上出现的各种着舰状况。在初始的基于计算机的试验中，发现F-35的机身出现裂缝，但是迅速对设计做出了调整。F-35的首次航母着舰试验计划于2012年进行，海军希望该型战机2016年能参与作战。中国国防科技信息网
    """
    question = """洛马公司已经开始对飞机进行应力测试，包括哪些内容"""

    mss = MaxSimSentence(content, question)
    doc, socre = mss.getSentence()
    print('\n'.join(doc),socre)