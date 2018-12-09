#encoding=utf-8
import codecs

class FileObj(object):

    def __init__(self,filepath):
        self.filepath = filepath

    # 按行读入数据，返回一个List
    def read_lines(self):
        self.sentences = []

        file_obj = codecs.open(self.filepath,'r','utf-8')
        while True:
            with open('./testQuestions.txt', 'w+', encoding='utf8') as w:
                line = file_obj.readline()
                line = line.strip('\r\n')
                w.write(line + '\n')
                if not line:
                    break
                self.sentences.append(line)
        file_obj.close()

        return self.sentences
