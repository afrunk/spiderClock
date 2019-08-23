# 图片爬虫
'''
一开始的想法是在数据库中添加一个标签属性 判断是否已经被下载
后来嫌太麻烦就作罢 现在看来还是得如此
思路：
- 通过标签从数据库中获取未被爬取得图片的存储地址、爬取url
- 多线程爬取所有的图片存入指定文件夹内

多进程 传值测试
from multiprocessing import Pool
import os, time, random

def long_time_task(name,test):
    print('Run task %s (%s) %s...' % (name, os.getpid(),test))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    test='测试传值'
    for i in range(5):
        p.apply_async(long_time_task, args=(i,test))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

'''


import requests
from bs4 import BeautifulSoup
import pymysql
import os
import time
from multiprocessing import Pool
# from multiprocessing import ProcessError as Pool
# 链接数据库 切换时候修改db即可
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='password',
                     db='digikeydata',
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
# 测试文件夹方法
def pathCreate():
    paths =['Audio Products/Alarms, Buzzers, and Sirens/668-1062-2-ND.JPG','Audio Products/Microphones/2104-MO044202-3-ND.JPG']
    for path in paths:
        pathlist = path.split('/')
        # print(pathlist)
        kind = pathlist[0]
        pakind = pathlist[1]
        imgname = pathlist[2]
        cur_dir = 'G:\Python_Data\ComputerDesig\spiderDigikey\\' + kind
        # print(cur_dir)
        cur_dir_1 = cur_dir + '\\' + pakind
        if os.path.isdir(cur_dir) == False:
            os.makedirs(kind)  # 需要在爬取一个新的类目时即创建文件夹
            # print(cur_dir_1)
            if os.path.exists(cur_dir_1) == False:
                os.makedirs(cur_dir_1)
        else:
            if os.path.exists(cur_dir_1) == False:
                os.makedirs(cur_dir_1)
        filename = cur_dir_1 + '\\' + imgname
        print(filename)


# 直接从数据库中读取图片链接和id下载下来然后存入三个文件夹下
def get_images_new(content):
    # i = 0  # 记录保存图片的页数
    # print("这一部分的字典是：")
    imageUrl = content[0]
    path = content[1]
    # imageUrl = 'media.digikey.com/photos/TDK%20Photos/PS1240P02AT.jpg'
    # path = 'Audio Products/Alarms, Buzzers, and Sirens/445-2525-3-ND.JPG'
    # print(imageUrl) # 图片链接
    # print(path) # 图片路径
    try:
        # 判断是否有图片 如果没有则不下载 如果有的话就
        if imageUrl != 'photo not available':
            # path = 'Audio Products/Alarms, Buzzers, and Sirens/668-1062-2-ND.JPG'
            pathlist = path.split('/')
            # print(pathlist)
            kind = pathlist[0]
            pakind = pathlist[1]
            imgname = pathlist[2]
            cur_dir = 'G:\Python_Data\ComputerDesig\spiderDigikey\\' + kind
            # print(cur_dir)
            cur_dir_1 = cur_dir + '\\' + pakind
            if os.path.isdir(cur_dir) == False:
                os.makedirs(kind)  # 需要在爬取一个新的类目时即创建文件夹
                # print(cur_dir_1)
                if os.path.exists(cur_dir_1) == False:
                    os.makedirs(cur_dir_1)
            else:
                if os.path.exists(cur_dir_1) == False:
                    os.makedirs(cur_dir_1)
            filename = cur_dir_1 + '\\' + imgname
            print(filename)
            respone = requests.get('https://'+imageUrl,headers=headers,timeout=5) # 超时2s就放弃
            fp = open(filename,'wb')
            fp.write(respone.content)
            fp.close()
            print("图片已经保存，路径是：%s,链接是：%s" %(filename,imageUrl))
            # 更新图片获取状态
            sql = "update newdata set imgGot = 1 where imageUrl='%s'" % (imageUrl)  # 如果已经被爬取过则修改 isOrNoGot 为 1
            try:
                cursor.execute(sql)  # 执行命令
                db.commit()  # 提交事务
            except:
                db.rollback()  # 回滚
            time.sleep(2)
    except:
        pass




# 多进程入口
def PoolDrive(Kind):
    # 请求图片链接存入字典
    urllist = []
    pathlist = []
    try:
        dict = {}
        # 查询的是保存爬取具体信息的页面

        sql = "select imageUrl,imageGot,imagesPath from newdata where imageGot='0' and imageUrl!='photo not available'  and Kind='%s'" %(Kind)  # 获取没有被爬取过的图片链接
        cursor.execute(sql)
        print(sql)
        # print(cursor.fetchone()[0])
        for i in cursor:
            imageUrl = i[0]
            path = i[2]
            # print(path)
            urllist.append(imageUrl)
            pathlist.append(path)
    except:
        print("导出失败，请联系技术！")
        pass
    print(urllist,pathlist)
    zip_args = list(zip(urllist, pathlist))  # 使用该方法来传递多个参数到多进程中去
    # print(zip_args)
    pool = Pool(processes=100)  # 设置多进程数量
    pool.map(get_images_new, zip_args)  # 注意此处只传入一个参数 其中包括了2个值
    pool.close()
    pool.join()

if __name__=='__main__':
    # 获取图片函数
    url=''
    # get_images_new(url)
    # 测试文件夹
    # pathCreate()
    # 头部
    Kind = input("请输入您要下载的图片所属类目：")
    # print(Kind)
    # PoolDrive(Kind)
    try:
        sql="select count(*) from newdata where imageGot='0' and imageUrl!='photo not available'  and Kind='%s'" % (Kind)
        cursor.execute(sql)
        print(cursor.fetchone()[0])
    except:
        pass


