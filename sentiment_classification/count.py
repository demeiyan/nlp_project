import re
if __name__ == '__main__':
    leng = 0
    dict = {}
    x_train=[]
    with open("dataset/test_x.txt","r+") as f:
        for line in f:
            print(line)
            list = re.split('\\s+', line.strip().strip('\n'))
            x_train.append(list)
            for index in list:
                if(index in dict):
                     dict[index] = dict[index]+1
                else:
                    dict[index] =1
            if len(list)>leng:
                leng = len(list)
    print(leng,end='')