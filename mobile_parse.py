
from fake_useragent import UserAgent
import os
import json
import logging

def parse_json(response):
    re_list = response["data"]["poiList"]
    totalCount = re_list["totalCount"]
    poiInfos = re_list["poiInfos"]
    result = dict()
    shops = []
    result["data"] = shops
    result["total"] = totalCount
    for item in poiInfos:
        data = dict()
        data["avgPrice"] = item["avgPrice"]
        data["avgScore"] = item["avgScore"]
        data["cateName"] = item["cateName"]
        data["frontImg"] = item["frontImg"]
        data["lat"] = item["lat"]
        data["lng"] = item["lng"]
        data["name"] = item["name"]
        data["id"] = item["poiid"]
        data["areaName"] = item["areaName"]
        data["ctPoi"] = item["ctPoi"]
        shops.append(data)
    return result

def parse_detail_html(html):
    prefix_str = "window._appState = "
    subfix_str = ";</script>"
    start_index = html.index(prefix_str)
    end_index = html.index(subfix_str, start_index)
    if start_index <= 0 or end_index <= 0:
       logging.warning("shop detail not found")
       return dict()
    detail = html[start_index+len(prefix_str):end_index]
    result = dict()
    result["phone"] = parse_phone(detail)
    result["openInfo"] = parse_open_info(detail)
    return result

def parse_phone(html):
    prefix_str = "phone\":\""
    subfix_str = "\","
    start_index = html.index(prefix_str)
    end_index = html.index(subfix_str, start_index)
    if start_index <= 0 or end_index <= 0:
       logging.warning("phone not found")
       return ""
    return html[start_index+len(prefix_str):end_index]

def parse_open_info(html):
    prefix_str = "openInfo\":\""
    subfix_str = "\","
    start_index = html.index(prefix_str)
    end_index = html.index(subfix_str, start_index)
    if start_index <= 0 or end_index <= 0:
       print("openInfo not found")
       return ""
    return html[start_index+len(prefix_str):end_index]

if __name__ == '__main__':
    demo_path = os.path.dirname(os.path.realpath(__file__)) + '/utils/demo.json'
    with open(demo_path, encoding='utf-8') as f:
        DEMO_RESPONSE = eval(f.read())
    result = parse_json(DEMO_RESPONSE)
    print(result["data"])

    demo_detail_path = os.path.dirname(os.path.realpath(__file__)) + '/utils/demo_detail.html'
    with open(demo_detail_path, encoding='utf-8') as f:
        DEMO_HTML = f.read()
    result = parse_detail_html(DEMO_HTML)
    print(result)

