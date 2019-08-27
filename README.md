### 抓取Digikey 网站全部电子元器件的具体信息
#### 主要设计技术
- python :基础语言
- BS4：分析HTML，提取我们所需要的信息
- request：发送伪造请求
- mysql:存储抓取到的数据
- Navicate:mysql 工具

[Digikey 美国电子商品](https://www.digikey.com/products/en)，我们需要爬取的内容如下图：<br>
![首页](https://github.com/afrunk/spiderClock/blob/master/OtherDoc/1.png)

![具体商品信息页](https://github.com/afrunk/spiderClock/blob/master/OtherDoc/2.png)

文件中的代码功能分类如下：
- spiderDigikeyMain.py：将第二张图片中的所有的信息，包括图片、分类等抓取到数据库中去，然后保存下来
- spiderImages.py:抓取图片的脚本，存入到以大类目\小类目的文件夹结构存储，图片的名字是 ID名
- selectCoregory.py：查询抓取到的类目的具体数量

主要思路如下：
- 在首页抓取所有的大类目下小类目的链接，然后抓取小类目的首页，将其转变成500一个商品的页面。再抓取500一个商品还需要多少翻页，进行for循环迭代之后将拼接成功的url链接存入到数据库的三个表中
- 从数据库的三个表中读取url链接传入抓取HTML页面的函数进行抓取，然后将抓到的数据传入到数据库的data表中，根据三个链接表构建三个不同的数据表
- 抓取数据完成之后，从data表中读取数据的图片链接和大类目小类目，新建大类目\小类目的文件夹，抓取图片存入其中

该网站的主要特色：
- 多线程大批量短时间请求大量数据并没有进行反爬
- 并不是所有的数据都可以请求到，同一个链接表需要进行多次重复抓取，需要主义主键的设置（mysql的主键唯一时，才能起到避免重复抓取的功能）
- 抓取数据和抓取同时进行的话速度奇慢，所以分开抓取。
- 数据量过大，总量在900万左右，需要构建不同的表来进行存储可能会提高查询和导出速率。

附上两张数据库表设计：

![](https://github.com/afrunk/spiderClock/blob/master/OtherDoc/3.png)

![](https://github.com/afrunk/spiderClock/blob/master/OtherDoc/4.png)

