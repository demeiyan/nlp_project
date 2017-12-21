# -*- coding: utf-8 -*-
import jieba
if __name__ == '__main__':
    seg = jieba.lcut("2015年9月16日，国务院总理李克强主持召开推进新型城镇化建设试点工作座谈会，在会上总理指出要通过新型城镇化建设，");
    print('/ '.join(seg))