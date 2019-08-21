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


if __name__ == "__main__":
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

    # start_3 = time.time()
    # pool = Pool(processes=10)
    # pool.map(re_scraper, urls)
    # end_3 = time.time()
    # print('10进程爬虫耗时:', end_3 - start_3)
