import json


import pymysql
import logging
from config import sqlConf

connect = pymysql.connect(**sqlConf)
TABLE = "meituan_restaurant"
json_path = ""


def create_db():
    sql = '''
            CREATE TABLE IF NOT EXISTS`meituan_restaurant` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `poiid` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `channel` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `cateName` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `avgScore` float DEFAULT NULL,
            `areaName` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `cityName` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `lat` float DEFAULT NULL,
            `lng` float DEFAULT NULL,
            `addr` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `abstracts` text COLLATE utf8mb4_unicode_ci,
            `openInfo` text COLLATE utf8mb4_unicode_ci,
            `phone` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `historyCouponCount` int(11) DEFAULT NULL,
            `introduction` text COLLATE utf8mb4_unicode_ci,
            `featureMenus` text COLLATE utf8mb4_unicode_ci,
            `ctPoi` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            `frontImg` varchar(256) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
            KEY `index_meituan_restaurant_poiid` (`poiid`),
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        '''.format(TABLE)
    cur = connect.cursor()
    cur.execute(sql)
    connect.commit()


def save(data):
    """存储数据"""
    print(data)
    try:
        sql = '''
            INSERT INTO `{}` (`poiid`, `channel`, `name`, `cateName`, `avgScore`, `areaName`, `cityName`, `lat`, `lng`, `frontImg`, `ctPoi`)
            VALUES
	        (%(poiid)s, %(channel)s, %(name)s, %(cateName)s, %(avgScore)s, %(areaName)s, %(cityName)s, %(lat)s, %(lng)s, %(frontImg)s, %(ctPoi)s)
            ON DUPLICATE KEY UPDATE poiid=poiid;
        '''.format(TABLE)
        cur = connect.cursor()
        cur.execute(sql, data)
        connect.commit()
    except Exception as e:
        logging.error("\nError: %s, Please check the error.\n" % e.args)

def build_item(data):
    item = dict()
    item['poiid'] = data['poiid']
    item['channel'] = data['channel']
    item['name'] =  data['name']
    item['cateName'] =  data['cateName']
    item['avgScore'] =  data['avgScore']
    item['areaName'] =  data['areaName']
    item['cityName'] =  "guangzhou"
    item['lat'] =  data['lat']
    item['lng'] =  data['lng']
    item['frontImg'] =  data['frontImg']
    item['ctPoi'] =  data['ctPoi']
    return item

def main():
    create_db()
    with open(json_path, encoding='utf-8') as f:
        infos = eval(f.read())
    # print(infos[0])
    for item in infos:
        save(build_item(item))

if __name__ == '__main__':
    main()