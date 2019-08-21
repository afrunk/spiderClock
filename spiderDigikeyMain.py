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

# 写入数据库操作
def write_database_operation(tdsList,itemAll):
    # for i in tdsList:
    #     print(i)
    print(len(tdsList))
    # print(itemAll)
    #mysql存储过程中用变量做表名
    print("成功链接数据库")
    try:
        sql = """
        INSERT IGNORE INTO NewData (Kind,PaKind,infourl,imageUrl,imagesPath,diginum,ManufacturePartNumber,Manufacturer,Description,QuantityAvailable,price,minmumQuantity,Series,ParaData) 
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"""\
        .format(tdsList[0],tdsList[1],tdsList[2],tdsList[3],tdsList[4],tdsList[5],tdsList[6],tdsList[7],tdsList[8],tdsList[9],tdsList[10],tdsList[11],tdsList[12],itemAll)
        print(sql)
        cursor.execute(sql) # 执行命令
        db.commit() # 提交事务
    except:
        pass


# 生成随机字符串为图片命名
# 直接放弃了 使用id作为图片命名
def create_random():
    # 生成随机图片名
    import random, string
    s = string.ascii_letters + string.digits
    print(s)

    n = [''.join(random.choices(s, k=12)) for I in range(60000)] #存储随机生成字符串的列表
    # print(n)
    return n


# 废弃
# 下载图片和返回给数据库一个图片的路径
# 传入大类目的名字 因为导出使用的是大类目 后续使用大类目作为文件夹名
# 图片的名字使用十二位随机字符串
# 访问速度 所以使用的新函数
# def get_images_No(folderName,imageUrl):
#     # 随机生成字符串
#     n =create_random()
#     # 保存文件夹的名字即我们的大目录名
#     daleimu =folderName
#     # 是否有图片 如果没有图片使用统一的默认无图片路径 如果有的话在爬取和存储
#     if imageUrl == 'photo not available':
#         filename = 'pna_en.jpg'
#     else:
#         # respone = requests.get('https://'+imageUrl,headers=headers)
#         dirname = daleimu
#         if os.path.exists(daleimu) == False:
#             os.makedirs(daleimu) #需要在爬取一个新的类目时即创建文件夹
#         filename = dirname +'/'+ n[0]+'.JPG'
#         print(filename)
#         # fp = open(filename,'wb')
#         # fp.write(respone.content)
#         # fp.close()
#     return filename


# 直接从数据库中读取图片链接和id下载下来然后存入三个文件夹下
def get_images_new():
    try:
        sql = 'select imgerUrl, from urlsOther ' #
        cursor.execute(sql)
        for i in cursor:
            if imageUrl == 'photo not available':
                filename = 'pna_en.jpg'
            else:
                respone = requests.get('https://'+imageUrl,headers=headers)
                filename = ID+'.JPG'
                print(filename)
                fp = open(filename,'wb')
                fp.write(respone.content)
                fp.close()
    except:
        pass

navigationBars = [] # 原属性栏列表
navigationBarsReally = [0,0,0,0,0] # 处理后属性栏列表 因为我们需要为前面的三个选项赋值 所以必须先定义
# 将页面的导航栏删除掉不需要的 以及将其处理成我们存入数据库的格式
def deal_navigation(navigationBars):
    # 处理导航栏
    item = ''
    navigationBars.pop(0)
    navigationBars.pop(0)
    navigationBars[6] = 'price'
    # print(navigationBars)
    # 未导航栏中没有但是数据库中有的栏目添加进列表前面
    navigationBarsReally[0] = 'Kine'  # 大类目
    navigationBarsReally[1] = 'MinKine'  # 小类目
    navigationBarsReally[2] = 'infoUrl'  # 详情页链接
    navigationBarsReally[4] = 'imagesPath' #图片路径
    navigationBarsReally[3] = 'imageUrl'
    for i in range(1,len(navigationBars)): # image 的 td不能删除 所以在这里直接掠过1
        if i < 9:
            # 将不变的导航栏写入新的列表
            navigationBarsReally.append(navigationBars[i])
        else:
            # print(navigationBars[i])
            stritem = navigationBars[i]
            item += "<|>" + navigationBars[i]

    # print(navigationBarsReally)
    # print(item)
    # 将处理好的导航栏属性 返回
    return navigationBarsReally,item

# 请求html文件
def get_html(url):
    content = requests.get(url, headers=headers)
    soup = BeautifulSoup(content.text, 'lxml')
    return soup

# 提取HTML的具体信息 处理后存入列表供写入数据库的函数调用
def get_html_sensor(url):
    print("正在爬取链接是："+url)
    soup=get_html(url)
    # 匹配类目
    hFirst = soup.find('h1').get_text()
    # print(hFirst)
    # print(hFirst.split(">"))
    hFirstList = hFirst.split(" > ")
    hFirstList.pop(0) # 分隔符提取出来选取后面两个属性
    # print(hFirstList)


    # 匹配导航栏
    tblheads = soup.find('thead')
    # print(tblheads)
    tr = tblheads.find('tr')
    ths = tr.find_all('th')
    for th in ths:
        # print(th.string)
        navigationBar =th.get_text().strip().strip()
        navigationBars.append(navigationBar)
        # print(navigationBar)
    navigationBarsReally,item=deal_navigation(navigationBars)


    # 提取具体的信息 ： 将数据处理成我们所需要的格式
    tbody = soup.find('tbody',id='lnkPart')
    itemscopes = tbody.find_all('tr')#获取每个商品的具体tr
    for itemscope in itemscopes:

        tds = itemscope.find_all('td')#获取每个属性的td
        # 删除掉导航栏的无用信息
        tds.pop(0)
        tds.pop(0)
        # 为了下一个商品的信息可以正常存入列表和字符串中，我们需要在下一次迭代前进行一个更新
        tdsList = [0,0]  # 存储具体信息的列表 方便写入数据库 因为我们直接赋值两个元素 所以需要先自定义 类似navigationBarsReally 的定义
        tdsItems = ''  # 存储具体的信息的字符串 方便写入数据库
        imagePath = ''
        # 将前面提取的类目存入tdsList
        tdsList[0] = hFirstList[0] # 大类目
        tdsList[1] = hFirstList[1] # 小类目
        for i in range(len(tds)):
            # 获取图片的下载链接、商品的具体链接、以及添加商品的保存路径
            # print(tdsList)
            if i == 0:
                try:
                    # 提取图片的链接和具体商品的详情页存入到列表中
                    infoUrl = 'https://www.digikey.com' + tds[i].find('a').get('href')
                    tdsList.append(infoUrl)
                    # print('InfoUrl 是否被抓取到 '+ infoUrl)
                    # 添加try 中 如果没有访问到 imgUrl 之后跳转到 except
                    imgUrl = tds[i].find('img', 'pszoomer').get('zoomimg').replace('//', '')
                    tdsList.append(imgUrl)
                    # print("当前是否访问到imgUrl")
                    # print(imgUrl)
                    # print("访问到了！")
                    # 下载图片 并将图片的下载路径传入
                    # imagePath = 'Testpath'
                    # imagePath = get_images(tdsList[0],imgUrl)
                    # # print(imagePath)
                    # tdsList.append(imagePath)
                except:
                    imgUrl= 'photo not available'
                    tdsList.append(imgUrl)
                    # imagePath = 'Testpath'
                    # tdsList.append(imagePath)
            elif i == 5 :
                # print(i)
                # print(tds[i])
                # 使用 replace去除掉html中的空格和回车
                try:
                    quantityAvailable = tds[i].find('span','desktop').get_text().replace('\n', ' ').replace('\r', ' ').strip()
                    # print(quantityAvailable)
                    tdsList.append(quantityAvailable)
                except:
                    quantityAvailable=''
                    tdsList.append(quantityAvailable)
            elif i == 7 :
                try:
                    quantityAvailable = tds[i].find('span', 'desktop').get_text().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()
                    # print(quantityAvailable)
                    tdsList.append(quantityAvailable)
                except:
                    quantityAvailable = ''
                    tdsList.append(quantityAvailable)


            elif 0 < i < 9 and i != 5  :
                tdsContent = tds[i].get_text().strip().strip().replace('Available:','').replace('Minimum:','')
                # print(tdsContent)
                tdsList.append(tdsContent)

            else:
                tdsContent = tds[i].get_text().strip().strip().replace('Available:', '').replace('Minimum:', '')
                # print(tdsContent)
                tdsItems += '<|>' + tdsContent

        # 图片的文件名为 ID + 'jpg'
        # 如果没有图片的话就直接保存 Test.jpg 文件
        if imgUrl == 'photo not available':
            imagePath = 'Test.jpg'
            print(imagePath)
            tdsList.insert(4, imagePath)

        else:
            imagePath =tdsList[0]+'/'+tdsList[1]+'/'+tdsList[4] +'.JPG'
            print(imagePath)
            tdsList.insert(4,imagePath)

        print(navigationBarsReally)
        print(tdsList)  # 存入到数据库的各个属性值
        # print(item)
        # print(tdsItems)
        itemAll = item +'                     '+tdsItems
        # print(itemAll)  # 存入到数据库的ParaData 即其他参数
        # print('*****************************')
        # 调用写入数据库的函数将值传入数据库
        # 必须在数据更新前进行写入操作
        write_database_operation(tdsList,itemAll)
    sql = "update urlsOther set isOrNoGot = 1 where url = '%s'" % (url)  # 如果已经被爬取过则修改 isOrNoGot 为 1
    try:
        cursor.execute(sql)  # 执行命令
        db.commit()  # 提交事务
    except:
        db.rollback()  # 回滚

    # 测试是否已经更改
    sql = "select * from urlsOther where url = '%s'" % (url)
    try:
        cursor.execute(sql)
        # print(cursor(0)) 不能使用这样子的方法来读取cursor()
        for i in cursor:
            print("更新后的数据：")
            print(i)
    except:
        pass


# 测试是否可以更新链接是否被爬取标记
def test_sql():
    # 当前页的爬取完成之后我需要进入表中更新当前链接的获取属性
    url = 'https://www.digikey.com/products/en/crystals-oscillators-resonators/crystals/171/page/101?FV=ffe001dd&quantity=0&ColumnSort=0&page=101&pageSize=500'
    sql= "update urlsFirst set isOrNoGot = 1 where url = '%s'" %(url) # 如果已经被爬取过则修改 isOrNoGot 为 1
    try:
        cursor.execute(sql) # 执行命令
        db.commit() # 提交事务
    except:
        db.rollback() # 回滚

    # 测试是否已经更改
    sql = "select * from urlsFirst where url = '%s'" %(url)
    try:
        cursor.execute(sql)
        # print(cursor(0)) 不能使用这样子的方法来读取cursor()
        for i in cursor:
            print("更新后的数据：")
            print(i)
    except:
        pass


# 获取链接函数
# 获取所有需要爬取的具体页面的链接存入txt文件
# 分为三个文件存储 即客户说的分三个数据库存储文件
def get_all_urls(url):
    # start = time.process_time()  # 开始时间
    htmlContent = get_html(url)
    ulsList = htmlContent.find_all('a', class_='catfilterlink')
    print(ulsList)
    # 最后一个是原链接 去掉
    ulsList.pop(-1)
    urlsList = []  # 存储访问页面的url
    for url in ulsList:
        urlProducts = 'https://www.digikey.com' + url.get('href')  # 构建url使得每次访问的页面都有500个商品
        print(urlProducts)
        urlsList.append(urlProducts)
    #     with open('urls.txt', 'a', encoding='utf-8') as f:
    #         f.write(urlProducts + '\n')
    #         f.close()

    for i in range(0, len(urlsList)):
        htmlDetailsPages = get_html(
            urlsList[i] + '?FV=ffe001dd&quantity=0&ColumnSort=0&page=1&pageSize=500')  # 添加后缀来计算500一页的商品有多少页
        # 访问页面 查看页数后是否还有数字
        span = htmlDetailsPages.find('span', class_='current-page')
        pages = span.get_text().replace('Page 1/', '').replace(',', '')  # 总共有多少页
        print(pages)
        print("原网页" + urlsList[i])
        if 'crystals-oscillators-resonators' in urlsList[i] or 'integrated-circuits-ics' in urlsList[i] or 'development-boards-kits-programmers' in urlsList[i] or 'switches' in urlsList[i]:
            for j in range(1, int(pages) + 1):
                # 拼凑可以直接访问下一页的链接
                newUrl = urlsList[i] + '/page/' + str(j) + '?FV=ffe001dd&quantity=0&ColumnSort=0&page=' + str(
                    j) + '&pageSize=500'
                urlsList.append(newUrl)
                print(newUrl)
                # 第一种保存链接方法 存入本地 txt
                # with open('urlFirst.txt', 'a', encoding='utf-8') as f:
                #     f.write(newUrl + '\n')
                #     f.close()

                # 第二种保存链接方法 存入数据库
                try:
                    sql = """
                    INSERT IGNORE INTO urlsFirst (url) 
                    VALUES('{}')""" \
                        .format(newUrl)
                    # print(sql)
                    print("正在插入链接到urlsFirst表中：" + newUrl)
                    cursor.execute(sql)
                    db.commit()
                except:
                    pass
        elif 'connectors-interconnects' in urlsList[i] or 'capacitors' in urlsList[i] or 'resistors' in urlsList[i]:
            for j in range(1, int(pages) + 1):
                # 拼凑可以直接访问下一页的链接
                newUrl = urlsList[i] + '/page/' + str(j) + '?FV=ffe001dd&quantity=0&ColumnSort=0&page=' + str(
                    j) + '&pageSize=500'
                urlsList.append(newUrl)
                print(newUrl)
                # 第一种保存链接方法 存入本地 txt
                # with open('urlSecond.txt', 'a', encoding='utf-8') as f:
                #     f.write(newUrl + '\n')
                #     f.close()
                # 第二种保存链接方法 存入数据库
                try:
                    sql = """
                        INSERT IGNORE INTO urlsSecond (url) 
                        VALUES('{}')""" \
                        .format(newUrl)
                    # print(sql)
                    print("正在插入链接到urlsSecond表中：" + newUrl)
                    cursor.execute(sql)
                    db.commit()
                except:
                    pass
        else:
            for j in range(1, int(pages) + 1):
                # 拼凑可以直接访问下一页的链接
                newUrl = urlsList[i] + '/page/' + str(j) + '?FV=ffe001dd&quantity=0&ColumnSort=0&page=' + str(
                    j) + '&pageSize=500'
                urlsList.append(newUrl)
                print(newUrl)
                # 第一种保存链接方法 存入本地 txt
                # with open('urlOthers.txt', 'a', encoding='utf-8') as f:
                #     f.write(newUrl + '\n')
                #     f.close()
                # 第二种保存链接方法 存入数据库
                try:
                    sql = """
                        INSERT IGNORE INTO urlsOther (url) 
                        VALUES('{}')""" \
                        .format(newUrl)
                    # print(sql)
                    print("正在插入链接到urlsOther表中："+newUrl)
                    cursor.execute(sql)
                    db.commit()
                except:
                    pass
    print(len(urlsList))
    # end = time.process_time()  # 结束时间
    # SpendTime = str(end - start)  # 测试整个程序运行的总时长
    # with open('urls.txt', 'a', encoding='utf-8') as f:
    #     f.write(SpendTime)
    #     f.close()

allUrls = []
# 读取链接函数存入列表方便多线程调用
def read_all_urls():
    # 废弃方法 不适合监测爬虫进度
    # 读取urls.txt 文件中的所有链接 封装成函数方便使用多线程
    # filenames = 'urlsTest.txt'
    # with open(filenames) as file_object:
    #     for content in file_object:
    #         # print(content.rsplit())
    #         allUrls.append(content.replace('\n',''))
    # return allUrls

    # 读取数据库的表文件 然后判断是否被爬取过 如果爬取过不写入列表 没有则写入
    sql = ('select * from urlsOther where isOrNoGot != 1')#表中所有信息读取所有信息 如果 isOrNoGot 不为 1 则获取
    # sql = ('select url from urlsFirst where isOrNoGot != 1') # 读取url 的信息
    cursor.execute(sql)
    urls = []
    for i in cursor:
        urls.append(i[0]) # 因为我只要第一个键的属性 即 url 所以直接存入列表元素的 0 即可
    print(urls)
    return urls

# 开始函数
# 使用多线程来测试反爬对于爬取速度的限制为多少
from multiprocessing import Pool
def get_url_content_test():
    #
    # 添加一个检测当前CPU核数的代码 将该数字填入到下面的代码中去实现自动的多线程爬取

    # 启动多线程爬取程序
    urls = read_all_urls()
    start_2 = time.time()
    pool = Pool(processes=1)
    pool.map(get_html_sensor, urls)
    end_2 = time.time()
    print('2进程爬虫耗时:', end_2 - start_2)

    # start_3 = time.time()
    # pool = Pool(processes=10)
    # pool.map(get_html_sensor, urls)
    # end_3 = time.time()
    # print('2进程爬虫耗时:', end_3 - start_3)

if __name__=='__main__':
    url= 'https://www.digikey.com/products/en'
    # 第一步 将所有得链接分类存储和保存在数据库中
    get_all_urls(url)
        # 测试读取数据库爬取链接代码
    # read_all_urls()
        # 测试更新数据库数据代码
    # test_sql()
    # 第二步 访问分类存储的链接 爬取之后标注为 1 默认值为0
    # get_url_content_test()
    # 第三步 多线程爬取图片存储在分类的文件夹下
    # get_images(folderName,imageUrl)
