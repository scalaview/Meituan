import requests
import json
import time
import random
import logging

from common import save, xdaili_proxy, abuyun_proxy
from mobile_parse import parse_json, parse_detail_html
from mobile_config import HEADERS, TIMEOUT, LIMIT, UUID, REQUEST_PAYLOAD, COOKIES, AREAS

url = 'https://meishi.meituan.com/i/api/channel/deal/list'


def shop_list(url, page):
    """商家列表"""
    # proxies = xdaili_proxy()
    # session = requests.Session()
    # response = json.loads(session.get(url, headers=HEADERS, proxies=proxies, timeout=TIMEOUT).text)
    # response = json.loads(requests.get(url, headers=HEADERS, timeout=TIMEOUT).text)
    request_payload = REQUEST_PAYLOAD.copy()
    request_payload["offset"] = page <= 0 ? 0 : (page - 1) * request_payload["limit"]
    response = requests.post(url, data=json.dumps(request_payload), headers=HEADERS, cookies=COOKIES)
    list_data = None
    for i in range(3):
        try:
            list_data = json.loads(response.text)
            break
        except Exception as e:
            logging.warning(e)
            time.sleep(random.randint(1,3))
    if list_data is None:
        logging.warning("can not parse data")
        return

    try:
        print(list_data)
        infos = parse_json(list_data)
        for info in infos["data"]:
            data = parse_json(info)
            print(data, sep='\n')
            try:
                save(data)
            except Exception as err:
                logging.warning("data save fail: {}".format(e))
        return infos["total"]
    except Exception as e:
        logging.warning(" Response status code: {}, Requests was found, no target data was obtained!".format(response['code']))


def main():
    list_url = 'https://meishi.meituan.com/i/api/channel/deal/list'
    for area in AREAS:
        area_id = area["id"]
        total = shop_list(list_url, 1)
        if total is None:
            continue
        max_pages = int(total/LIMIT)
        if total % LIMIT != 0:
            max_pages = max_pages + 1
        time.sleep(random.randint(3, 5))
        for page in range(2, 4):
            shop_list(list_url, page)
            time.sleep(random.randint(3, 5))

if __name__ == '__main__':
    main()