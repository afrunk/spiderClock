### Digikey 网站全部电子元器件的具体信息
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
- 
