# 爬取的时候需要修改的地方
'''
- 表名：
 - get_html_sensor() 函数中更新链接状态
 - read_all_urls() 获取链接存入数据
 - get_images_new() 获取图片链接
'''

import requests
from bs4 import BeautifulSoup
import pymysql
import os
import time

# 链接数据库 切换时候修改db即可
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='password',
                     db='digikeyfirst',
                     charset='utf8')
cursor = db.cursor()

# 请求头部
headers ={
        'authority':'www.digikey.com',
        'method':'GET',
        'path':'/products/en/audio-products/accessories/159',
        'scheme':'https',
        'https':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-HK,zh;q=0.9,zh-CN;q=0.8,en;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'cache-control':'max-age=0',
        'cookie':"instart_html_streaming=false; instart_reload_reason=10; instart_reload_additional_info=Intercepted function: querySelector On: [object HTMLDocument] of type: #document with selectors: div.homepage-featured__content > div.featured-content:last-child; csscxt=399247882.20480.0000; dtCookie=E593B64A943DF4BCEC8334D12DCE8769|X2RlZmF1bHR8MQ; TS01cecf1b=01460246b6c2e35404c26799fba2a10822329b78e13676af38990f16ea078c5c99fb386e9a029d91a2397ea30cb5d5fe62385115a4; TS0138bc45=01460246b6c67ca8f8d8a1bf49ea3d6b00adb9f25d7d40b542edf7c7e353f23fc2ee2b03440552ec11384e0eea1e2b13170be06ab7; pf-accept-language=en-US; ping-accept-language=en-US; TS0184e6b9=01460246b63256f943044cc114a6b76032d812898d9355edde17f55a219c1a72a0d98bb4d39176c46b207b4f2f0431265d08c248f1; i10c.ss=1566047760615; i10c.uid=1566047760617:1662; optimizelyEndUserId=oeu1566047761611r0.9361870224501541; EG-U-ID=D8ae9e2fda-fe35-481c-aadf-d8caf7926d1c; EG-S-ID=E861866b1c-ad90-49ee-ab82-367ee49fcb6c; _ga=GA1.2.2085766613.1566048334; _gid=GA1.2.310825462.1566048334; _msuuid_27490huz44870=44703864-FB2B-46FD-BB87-F79ECC5276D9; _evga_8774=3a916442c95712cc.; TS017613a9=01460246b625607c93ebeea121aa44b919377e5316c586db54cd585a8211b120c38a8ffdcd138425e7c8fe1a1bb0907e70062bcfbd; WRIgnore=true; TS013c3a0b=01460246b64198bd3f88181bd3a285e5cc9b890647a041ee5e3628871d42945519c9be001f7f567a3df7d4a461e63c14ce29ce0315; TS018060f7=01460246b68cd723277b854f22d3b68024f139adb71fc769c679e3b46b517ea1998a19d1348966a5fc96fcc4f583ba562d444eef9e; _aa7988=1x9a62; utag_main=v_id:016c9fb89b59001609e768ce2cc803073006206b00bd0$_sn:2$_ss:0$_st:1566056404179$ses_id:1566054142565%3Bexp-session$_pn:2%3Bexp-session; website#lang=; TS01d239f3=01460246b619af0364be922e0e3e45fc7326eaf281031c7f705e6aab6c6f062b13012669c1e19c75abc7c03afddb3be01e5458304c; TS01d5128f=01460246b60fe611ec18383c61ab63da1cec4e0a0f21627d14e8a2c059bf7575702c9322029da4c4ae2651fd0ce7479e1f978fa3b3; _gat_Production=1; QSI_HistorySession=https%3A%2F%2Fwww.digikey.com%2Fproducts%2Fen%2Fintegrated-circuits-ics%2Fclock-timing-clock-buffers-drivers%2F764%2Fpage%2F2~1566048340828%7Chttps%3A%2F%2Fwww.digikey.com%2Fproducts%2Fen%2Faudio-products%2Faccessories%2F159~1566049192229%7Chttps%3A%2F%2Fwww.digikey.com%2Fproducts%2Fen~1566054611170; __CT_Data=gpv=4&ckp=tld&dm=digikey.com&apv_53368_www=8&cpv_53368_www=4; utm_data_x=part_family%3DAccessories%2Chtml_element1%3Dcatfilterlink%2Chtml_element2%3D%2Chtml_element3%3Dcatfiltersub%2Cref_page_type%3DPS%2Cref_page_sub_type%3DCAT%2Cref_page_id%3DCAT%2Cref_page_event%3DSelect%20Family%2Chtml_element4%3DproductIndexList%2Cundefined%3Dcontent-container%2CExtRun%3D409.1%2Cccookie%3D2019-08-17T13%3A25%3A33.869Z%2CExtRun%3D409.1%7C428.1%7C357.5; ctm={'pgv':7574547137797923|'vst':2385523260024033|'vstr':4532683176955253|'intr':1566054655450|'v':1|'lvst':53}; i10c.uservisit=17; i10c.bdddb=c2-e665bBx4YeKyjjpB3dTkLGukvWtNTo20TLztSTnuSVwL1xuo56foG0jkv6tMv5vYDDvpPSGkO8sM36oGYzYkn8epvRzuxs55VDvPPRi1bSsMt3RFt48fL0r2qWyHwR5vUsqpUozFJXsHzarByeTkLAOehGaHvtx12Gqp4MiplheEjtoGyzZIMvjPqWyjARsfPIvkVzlnPdzHycoGyOgfL0eqTUtMVo20pbqpUMjNQdnMYxtGKprWtbepvRzuto2aPIvE6HdpOStut7SBy4yukG6GqWyHwRx0UIqp7QdpOSswt2tWIITkLvkNqWyKqtfyPIvkU1dpOq8hGxtGt56fL0hkv9wHvtx55DvPPRi8A5TyZxtGt56iG0JkvWOWqt2vVqqpUMlONatQt2TF19bfLaittZtMVs61VDvPTVmnJXSL29sByeXpL6epVV3P0o2aTN1wPRIoUWvH1doGyzYKG0jHBRyMquazZDvPPRiGDPiDt2tBzcWfLaepvgh2Vbx0UDwNSMiPJXsl8xtGt56iG0JkvWNjqt2vVqqpUMiqJYRHyeoGyzdL",
        'referer':'https://www.digikey.com/products/en/audio-products/accessories/159',
        'sec-fetch-mode':'navigate',
        'sec-fetch-site':'same-origin',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }




def get_index_url(url):
    htmlContent = get_html(url)
    ulsList = htmlContent.find_all('a', class_='catfilterlink')  # catfilterlink
    # print(ulsList)
    # 最后一个是原链接 去掉
    ulsList.pop(-1)
    urlsList = []  # 存储访问页面的url
    for url in ulsList:
        urlProducts = 'https://www.digikey.com' + url.get('href')  # 构建url使得每次访问的页面都有500个商品
        # print(urlProducts)
        urlsList.append(urlProducts)
    urlsList.pop(-1)
    return urlsList

# 请求html文件
def get_html(url):
    NETWORK_STATUS = True
    print(url)
    try:
        content = requests.get(url, headers=headers,timeout=10)
        if content.status_code == 200:
            soup = BeautifulSoup(content.text, 'lxml')
            return soup
    except requests.exceptions.Timeout:
        NETWORK_STATUS = False
        if NETWORK_STATUS == False:
            for i in range(1,10):
                try:
                    response = requests.get(url, headers=headers,timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'lxml')
                        return soup
                except requests.exceptions.ConnectionError as e:
                    print(e)




# 获取链接函数
# 获取所有需要爬取的具体页面的链接存入txt文件
# 分为三个文件存储 即客户说的分三个数据库存储文件
def get_all_urls(urlsList):
    # start = time.process_time()  # 开始时间

    #     with open('urls.txt', 'a', encoding='utf-8') as f:
    #         f.write(urlProducts + '\n')
    #         f.close()
    # 遍历首页获取到的所有链接进行插入

    # 多表查询
    """
    # 添加一个判断链接是否已经存在的值 如果已经存在则不不需要进行爬取的下一步
    testUrl=urlsList[i]+ '?FV=ffe001dd&quantity=0&ColumnSort=0&page=1&pageSize=500'
    # testUrl= 'https://www.digikey.com/products/en/audio-products/accessories/159/page/1?FV=ffe001dd&quantity=0&ColumnSort=0&page=1&pageSize=500'
    print(testUrl)
    # sql = "select count(*) from urlsFirst where url='%s'" % (testUrl) # 从一个表中查询
    sql="select * from urlsFirst where url='%s' union select * from urlsSecond where url='%s' union select * from urlsOther where url='%s'" %(testUrl,testUrl,testUrl)
    cursor.execute(sql)
    print(cursor.fetchone())
    # print(list(cursor.fetchone()[0])) # 输出查询到的数字的类型
    if(cursor.fetchone() == None):
        print("数据库中已经存在"+urlsList[i])
        continue # 使用continue 跳出当前if循环 使用break 可以跳出当前 for 循环
    else:
    """
    print("当前爬取的链接是多少："+urlsList)
    htmlDetailsPages = get_html(
        urlsList + '?FV=ffe001dd&quantity=0&ColumnSort=0&page=1&pageSize=500')  # 添加后缀来计算500一页的商品有多少页
    # 访问页面 查看页数后是否还有数字
    try:
        hFirst = htmlDetailsPages.find('h1').get_text()
        # print(hFirst)
        # print(hFirst.split(">"))
        hFirstList = hFirst.split(" > ")
        hFirstList.pop(0)  # 分隔符提取出来选取后面两个属性
        print(hFirstList)


        span = htmlDetailsPages.find('span', class_='current-page')
        pages = span.get_text().replace('Page 1/', '').replace(',', '')  # 总共有多少页
        print(pages)
        # print("原网页" + urlsList[i])
        if 'Crystals, Oscillators, Resonators' == hFirstList[0] or 'Integrated Circuits (ICs)' == hFirstList[0] or \
                'Development Boards, Kits, Programmers' == hFirstList[0] or 'Switches' == hFirstList[0]:
            for j in range(1, int(pages) + 1):
                # 拼凑可以直接访问下一页的链接
                newUrl = urlsList + '/page/' + str(j) + '?FV=ffe001dd&quantity=0&ColumnSort=0&page=' + str(
                    j) + '&pageSize=500'
                # urlsList.append(newUrl)
                print(newUrl)
                # 第一种保存链接方法 存入本地 txt
                # with open('urlFirst.txt', 'a', encoding='utf-8') as f:
                #     f.write(newUrl + '\n')
                #     f.close()

                # 第二种保存链接方法 存入数据库
                try:
                    sql = """
                        INSERT IGNORE INTO urlsFirst(url,Kind) 
                        VALUES('{}','{}')""" \
                        .format(newUrl,hFirstList[0])
                    # print(sql)
                    print("正在插入链接到urlsFirst表中：" + newUrl)
                    cursor.execute(sql)
                    db.commit()
                except:
                    pass
        elif 'Connectors, Interconnects' == hFirstList[0] or 'Capacitors' == hFirstList[0]  or 'Resistors' == hFirstList[0]:
            for j in range(1, int(pages) + 1):
                # 拼凑可以直接访问下一页的链接
                newUrl = urlsList + '/page/' + str(j) + '?FV=ffe001dd&quantity=0&ColumnSort=0&page=' + str(
                    j) + '&pageSize=500'
                # urlsList.append(newUrl)
                print(newUrl)
                # 第一种保存链接方法 存入本地 txt
                # with open('urlSecond.txt', 'a', encoding='utf-8') as f:
                #     f.write(newUrl + '\n')
                #     f.close()
                # 第二种保存链接方法 存入数据库
                try:
                    sql = """
                            INSERT IGNORE INTO urlsSecond(url,Kind) 
                            VALUES('{}','{}')""" \
                        .format(newUrl, hFirstList[0])
                    # print(sql)
                    print("正在插入链接到urlsSecond表中：" + newUrl)
                    cursor.execute(sql)
                    db.commit()

                except:
                    pass
        else:
            for j in range(1, int(pages) + 1):
                # 拼凑可以直接访问下一页的链接
                newUrl = urlsList + '/page/' + str(j) + '?FV=ffe001dd&quantity=0&ColumnSort=0&page=' + str(
                    j) + '&pageSize=500'
                # urlsList.append(newUrl)
                print(newUrl)
                # 第一种保存链接方法 存入本地 txt
                # with open('urlOthers.txt', 'a', encoding='utf-8') as f:
                #     f.write(newUrl + '\n')
                #     f.close()
                # 第二种保存链接方法 存入数据库
                # try:
                sql = """
                    INSERT IGNORE INTO urlsOther(url,Kind) 
                    VALUES('{}','{}')""" \
                    .format(newUrl, hFirstList[0])
                print(sql)
                # print("正在插入链接到urlsOther表中：" + newUrl)
                cursor.execute(sql)
                db.commit()
                # except:
                #     pass
        # print(len(urlsList))
        # end = time.process_time()  # 结束时间
        # SpendTime = str(end - start)  # 测试整个程序运行的总时长
        # with open('urls.txt', 'a', encoding='utf-8') as f:
        #     f.write(SpendTime)
        #     f.close()
    except:
        # print()
        with open('log-html.txt', 'a', encoding='utf-8') as f:
            f.write( urlsList + '\n')
            f.close()
    time.sleep(5)



from multiprocessing import Pool
if __name__=='__main__':
    # 先看日志中是否有未抓取到的 如果没有的话就代表着第一次抓取 直接抓取所有的链接 抓取完之后再跑一次 重新抓取log日志中的链接
    urls = []
    # 第二次跑 看log-url.txt 是否有写入的未抓取到的链接
    f = open("log-html.txt")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        # print(line,)  # 后面跟 ',' 将忽略换行符
        print(line, end='')  # 在 Python 3 中使用
        urls.append(line.replace('\n', ''))
        line = f.readline()
    f.close()
    print(urls)

    if(len(urls) < 1):
        # 第一次跑 跑完之后跑第二次
        url = 'https://www.digikey.com/products/en'
        urls=get_index_url(url)
    pool = Pool(processes=10)
    pool.map(get_all_urls, urls)  # 爬数据
    pool.map(get_all_urls, urls)#爬链接

