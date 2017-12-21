

"""
读取test.txt文件中的答案序列
"""
if __name__ == "__main__":
    with open("./data/test.txt", "r+", encoding="utf-8") as f:
        with open('out.txt', 'w+', encoding="utf-8") as f1:
            for i in range(2040):
                for j in range(6):
                    line = f.readline().strip()
                    if line[0:1] == 'R' or line[0:1] == 'r':
                        f1.write(str(j-2)+"\n")

