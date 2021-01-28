# -*- coding:utf-8 -*-

import requests
from pyquery import PyQuery as pq
import hashlib
import pymysql
# from sqlalchemy import create_engine
import pymysql
import pandas as pd
import logging
import random
import json
from config import *
import re

connect = pymysql.connect(**sqlConf)

def get_cities():
    """城市名称-拼音简写对照字典"""
    doc = pq(requests.get('https://www.meituan.com/changecity/').text)
    a_lists = doc('.cities a').items()
    cities = {}
    [cities.update({a.text(): a.attr('href').replace('.', '/').split('/')[2]}) for a in a_lists]
    print(cities)
    with open('./utils/cities.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(cities, indent=2, ensure_ascii=False))

def get_uuid():
    """获取uuid"""
    url = 'https://gz.meituan.com/meishi/'
    # url = "http://localhost:8050/render.html?url=https://bj.meituan.com/meishi/&wait=5"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    res = requests.get(url, headers=headers).text
    uuid = re.findall(r'"uuid":"(.*?)"', res, re.S)[0]
    with open('./utils/uuid.log', 'w') as f:
        f.write(uuid)

# engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USER, PASS, HOST, PORT, DB))

def create_db():
    sql = '''
            CREATE TABLE IF NOT EXISTS `{}` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `detail` VARCHAR(128) COLLATE utf8mb4_unicode_ci,
            `title` VARCHAR(256) COLLATE utf8mb4_unicode_ci,
            `avgprice` bigint(20) DEFAULT NULL,
            `avgscore` double DEFAULT NULL,
            `comments` bigint(20) DEFAULT NULL,
            `openInfo` VARCHAR(256) COLLATE utf8mb4_unicode_ci,
            `phone` VARCHAR(256) COLLATE utf8mb4_unicode_ci,
            `frontimg` VARCHAR(256) COLLATE utf8mb4_unicode_ci,
            `address` VARCHAR(256) COLLATE utf8mb4_unicode_ci,
            KEY `index_{}_detail` (`detail`),
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        '''.format(TABLE)
    cur = connect.cursor()
    cur.execute(sql)
    connect.commit()

def save(data):
    """存储数据"""
    try:
        sql = '''
            INSERT INTO `{}` (`detail`, `title`, `avgprice`, `avgscore`, `comments`, `frontimg`, `address`)
            VALUES
	        (%(detail)s, %(title)s, %(avgprice)s, %(avgscore)s, %(comments)s, %(frontimg)s, %(address)s)
            ON DUPLICATE KEY UPDATE detail=detail;
        '''.format(TABLE)
        cur = connect.cursor()
        cur.execute(sql, data)
        connect.commit()
    except Exception as e:
        logging.error("\nError: %s, Please check the error.\n" % e.args)
        _ = e

def get_md5(url):
    """md5处理"""
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def xdaili_proxy():
    results = requests.get(url=API).json()['RESULT']
    agents = ["http://{}:{}".format(res['ip'], res['port']) for res in results]
    proxies = {
        "http": random.choice(agents),
        "https": random.choice(agents)
    }
    return proxies

def abuyun_proxy():
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": PROXY_HOST,
        "port": PROXY_PORT,
        "user": PROXY_USER,
        "pass": PROXY_PASS,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies

if __name__ == '__main__':
    # get_cities()
    get_uuid()