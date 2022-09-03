import requests
import json
from pymysql import *


# 连接数据库的方法
def connectDB():
    try:
        db = connect(host='localhost', port=3306, user='root', password='123456', db='db')
        print("数据库连接成功")
        return db
    except Exception as e:
        print(e)
    return NULL


db = connectDB()


# 向数据库中插入数据的方法
def insertInformation(db, table, Date, Province, City, Confirmed_num, Yisi_num, Cured_num, Dead_num, Code):
    cursor = db.cursor()
    try:
        cursor.execute(
            "insert into %s(Date,Province,City,Confirmed_num,Yisi_num,Cured_num,Dead_num,Code) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            table, Date, Province, City, Confirmed_num, Yisi_num, Cured_num, Dead_num, Code))
        print("插入成功")
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        print(e)
        db.rollback()
    return False


def queryInformation(city):
    cursor = db.cursor()
    sql = "SELECT * FROM info WHERE City =  '%s'" % (city)
    try:
        # print(sql)
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchone()
        return results[-1]
    except Exception as e:
        print(e)
        db.rollback()


def clearTable(date):
    cursor = db.cursor()
    sql = "delete from info2 where Date = '%s'" % (date)
    try:
        print(sql)
        # 执行SQL语句
        cursor.execute(sql)
    except Exception as e:
        print(e)
        db.rollback()


def get_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    json_text = requests.get(url).json()
    data = json.loads(json_text['data'])
    update_time = data['lastUpdateTime']
    all_counties = data['areaTree']
    all_list = []
    for country_data in all_counties:
        if country_data['name'] == '中国':
            all_provinces = country_data['children']
            for province_data in all_provinces:
                province_name = province_data['name']
                all_cities = province_data['children']
                for city_data in all_cities:
                    city_name = city_data['name']
                    city_total = city_data['total']
                    province_result = {'province': province_name, 'city': city_name, 'update_time': update_time}
                    province_result.update(city_total)
                    all_list.append(province_result)

    clearTable(all_list[0].get("update_time"))
    for info in all_list:
        print(info)
        insertInformation(db, "info2", info.get("update_time"), info.get("province"), info.get("city"),
                          info.get("confirm"), info.get("suspect"), info.get("heal"), info.get("dead"),
                          queryInformation(info.get("city")))


if __name__ == '__main__':
    get_data()
