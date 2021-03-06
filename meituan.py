#  -*- coding:utf-8 -*-

from token_ import encrypt_token
from urllib.parse import urlencode
from common import save, xdaili_proxy, abuyun_proxy
from parse import parse_json
import logging
import json
import requests
import time
import random
import multiprocessing
from config import GET_PARAM, HEADERS, TIMEOUT, MAX_PAGES, BASE_URL, DATA
from mobile_config import AREAS
# from visual import View

def main(base_url, areaId, page):
    """主函数"""
    # 添加_token参数
    data = GET_PARAM.copy()
    data["areaId"] = str(areaId)
    data["_token"] = encrypt_token(data)
    data['page'] = str(page)
    url = base_url + urlencode(data)
    # proxies = xdaili_proxy()
    # session = requests.Session()
    # response = json.loads(session.get(url, headers=HEADERS, proxies=proxies, timeout=TIMEOUT).text)
    response = json.loads(requests.get(url, headers=HEADERS, timeout=TIMEOUT).text)
    try:
        infos = response['data']['poiInfos']
        for info in infos:
            data = parse_json(info)
            print(data, sep='\n')
            save(data)
    except Exception as e:
        logging.warning(" Response status code: {}, Requests was found, no target data was obtained!".format(response['code']))
        _ = e

if __name__ == '__main__':
    # 多进程
    # pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # for page in range(1, MAX_PAGES + 1):
    #     pool.apply_async(main, (BASE_URL, page))
    # pool.close()
    # pool.join()
    for area in AREAS:
        area_id = area["id"]
        # 获取数据
        for page in range(1, MAX_PAGES + 1):
            main(BASE_URL, area_id, page)
            time.sleep(random.randint(1,3))

    # 可视化分析
    # view = View()
    # view.meishi_top10()
    # view.avgprice_comments()
    # view.avgscore_ratio()
    # view.wrodcloud()
