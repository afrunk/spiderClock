# Test - one
# 简单的多进程的实践代码 但是不能很好的反应当前进程所访问的链接是什么 不利于配合数据库进行监测爬虫的进度
import re
import time
from multiprocessing import Pool
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
}

def re_scraper(url):
    res = requests.get(url, headers=headers)

    print(res.content)
def startApp():
    # re_scraper("https://www.qiushibaike.com/8hr/page/1/")
    urls = ["https://www.qiushibaike.com/8hr/page/{}/".format(str(i)) for i in range(1, 35)]
    print(urls)
    start_1 = time.time()
    for url in urls:
        re_scraper(url)
    end_1 = time.time()
    print('串行爬虫时间:', end_1 - start_1)


    # start_2 = time.time()
    # pool = Pool(processes=2)
    # pool.map(re_scraper, urls)
    # end_2 = time.time()
    # print('2进程爬虫耗时:', end_2 - start_2)



# Test - two
# 探索如何将数据库中的链接与多线程结合起来 当多线程访问数据库的链接时 即进行返回
from multiprocessing import Process,Lock,Manager
import time
def sayhi(name,n):
    time.sleep(2)
    print("hello my name is %s" %name,n)
if __name__ == "__main__":
    for i in range(0,10):
        time.sleep(0.1)
        p=Process(target = sayhi,args =('mike' , i)) # 生成i个进程
        p.start()

# Test - three
# 这样子就可以直接使用前面的Test- one 的代码直接使用线性池来提高速度
# - 仍然是从数据库中读取一个表中的所有数据，如果所有的链接已经被爬取那么就不存入链接池，否则存入
# - 在每次的爬取完成之后进行标注 在表中将当前链接的后缀标注为 1