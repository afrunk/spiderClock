# 查询的脚本

import pymysql
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='password',
                     db='digikeydata',
                     charset='utf8')
cursor = db.cursor()
def get_category_num(category):
    # category ='Alarms, Buzzers, and Sirens'
    data = 'data'
    try:
        sql = "select count(*) from %s where Kind='%s'" %(pymysql.escape_string(data),category) # 注意 必须将where 后的属性和等号放在一起才可以
        print(sql)
        cursor.execute(sql)
        print(cursor.fetchone())
    except:
        print("查询不到，谢谢")
if __name__=='__main__':
    # cmd输入需要查询的类型
    category=input("请输入需要查询的类目:")
    while(category):
        get_category_num(category)
        category=input("请输入需要查询的类目:")