urls = []
# 第二次跑 看log-url.txt 是否有写入的未抓取到的链接
f = open("log-url.txt")  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方法
while line:
    # print(line,)  # 后面跟 ',' 将忽略换行符
    print(line, end = '')   # 在 Python 3 中使用
    urls.append(line.replace('\n',''))
    line = f.readline()
print(urls)
f.close()