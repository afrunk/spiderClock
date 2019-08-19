## 2019-8-18
'''
完成任务：
- 获取到页面的内容并且进行了解析提取

难点1：即便是一个类目下的商品信息的导航栏也是不同的如何将信息存入数据库对应的列呢？ 2019-8-19解决
- 我首先需要提取出来所有的商品信息的导航栏进行设计表：需要添加大类目、小类目的列名 这个需要有条理的添加 （程序设计的部分）
- 我需要将所有的页面的导航栏的信息提取出来之后存入一个列表，然后再写入数据库的时候调用该列表填充该写入的列名以实现各个列都可以相对应的填充



难点2：如何去实现断点续传呢？
将需要爬取的数据的链接即大类目、小类目的链接分类，爬取好了之后写入到本地的日志中
如果完成了某一部分的爬取效果之后将该类目从该日志中删除掉
然后将每一个类目的爬取日志都写入到本地
如果在其中发现了问题 则进行自动查询

难点3：如何实现大批量的数据爬取速度快且不被反爬
？

难点4：如何

解决途径：
    首先需要学习 python 的程序设计，这个可以参考 《python从入门到实践》这本书
    然后不断地简洁 码云、Github上地项目，同时将本项目 Push 到 Github 上去
    通过 Github 来记录学习过程

'''

## 2019-8-19
'''
完成任务：
- 完成导航栏的不同类型匹配，将其处理成合适的格式
    
    处理后列表属性值           含义                       完成度 
    diginum                 Digi-Key Part Number        1
    ManufacturePartNumber   Manufacturer Part Number    1
    PaKind                  小类目                       1
    Kind                    大类目                       1
    QuantityAvailable       Quantity Available          1
    Manufacture             Manufacturer                1
    Description             Description                 1
    Price                   price                       1
    Series                  Series                      1
    infourl                 详情链接页                   1
    PicName                 图片链接                     1
    ParaData                其他参数项                   1
    minmumQuantity          Minimum Quantity            1

建表属性顺序-和爬取得到的元素列表相对应
    id
    Kind
    PaKind 
    infourl
    PicName
    diginum 
    ManufacturePartNumber
    Manufacturer
    Description
    QuantityAvailable
    Price
    minmumQuantity
    Series
    ParaData



'''
import requests
from bs4 import BeautifulSoup

navigationBars = [] # 原属性栏列表
navigationBarsReally = [0,0,0] # 处理后属性栏列表 因为我们需要为前面的三个选项赋值 所以必须先定义


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
    for i in range(len(navigationBars)):
        if i < 9:
            # 将不变的导航栏写入新的列表
            navigationBarsReally.append(navigationBars[i])
        else:
            # print(navigationBars[i])
            stritem = navigationBars[i]
            item += "----" + navigationBars[i]

    # print(navigationBarsReally)
    # print(item)
    # 将处理好的导航栏属性 返回
    return navigationBarsReally,item

# 提取HTML的具体信息 处理后存入列表供写入数据库的函数调用
def get_html_sensor(url):
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

    content = requests.get(url,headers=headers)
    soup = BeautifulSoup(content.text,'lxml')

    # 匹配类目
    hFirst = soup.find('h1').get_text()
    # print(hFirst)
    # print(hFirst.split(">"))
    hFirstList = hFirst.split(">")
    hFirstList.pop(0) # 分隔符提取出来选取后面两个属性


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
        tds.pop(0)
        tds.pop(0)
        tdsList = [0,0]  # 存储具体信息的列表 方便写入数据库 因为我们直接赋值两个元素 所以需要先自定义 类似navigationBarsReally 的定义
        tdsItems = ''  # 存储具体的信息的字符串 方便写入数据库
        # 将前面提取的类目存入tdsList
        tdsList[0] = hFirstList[0] # 大类目
        tdsList[1] = hFirstList[1] # 小类目
        for i in range(len(tds)):
            # 获取图片路径
            if i == 0:
                try:
                    # 提取图片的链接和具体商品的详情页存入到列表中
                    imgUrl = tds[i].find('img', 'pszoomer').get('zoomimg').replace('//', '')
                    infoUrl = 'https://www.digikey.com'+ tds[i].find('a').get('href')
                    # print(imgUrl)
                    # print(infoUrl)
                    tdsList.append(infoUrl)
                    tdsList.append(imgUrl)

                except:
                    pass
            elif i == 5 :
                # print(i)
                # print(tds[i])
                # 使用 replace去除掉html中的空格和回车
                quantityAvailable = tds[i].find('span','desktop').get_text().replace('\n', ' ').replace('\r', ' ').strip()
                # print(quantityAvailable)
                tdsList.append(quantityAvailable)
            elif i == 7 :
                quantityAvailable = tds[i].find('span', 'desktop').get_text().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()
                # print(quantityAvailable)
                tdsList.append(quantityAvailable)
            elif 0 < i < 9 and i != 5  :
                tdsContent = tds[i].get_text().strip().strip().replace('Available:','').replace('Minimum:','')
                # print(tdsContent)
                tdsList.append(tdsContent)

            else:
                tdsContent = tds[i].get_text().strip().strip().replace('Available:', '').replace('Minimum:', '')
                # print(tdsContent)
                tdsItems += '----' + tdsContent
        print(navigationBarsReally)
        print(tdsList)
        # print(item)
        # print(tdsItems)
        itemAll = item +'                     '+tdsItems
        print(itemAll)
        print('*****************************')


if __name__=='__main__':
    # url = 'https://www.digikey.com/products/en/audio-products/accessories/159?FV=ffe0009f&quantity=0&ColumnSort=0&page=1&pageSize=500'
    # url = 'https://www.digikey.com/products/en/battery-products/batteries-non-rechargeable-primary/90'
    url='https://www.digikey.com/products/en/audio-products/alarms-buzzers-and-sirens/157?FV=ffe0009d&quantity=0&ColumnSort=0&page=1&pageSize=500'
    get_html_sensor(url)

