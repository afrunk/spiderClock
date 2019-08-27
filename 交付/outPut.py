import pymysql
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='password',
                     db='digikeyfirst',
                     charset='utf8')
cursor = db.cursor()

Kind = input("请输入要导出的类目：")
numbers = int(input("请输入要导出的数量："))
sql="select * from data where Kind ='%s' and dianpu1!=0 limit '%d'" %(Kind,numbers) #dianpu1 后续需要更换为具体的店铺名
cursor.execute(sql)
