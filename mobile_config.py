# -*- coding:utf-8 -*-

from fake_useragent import UserAgent
import random
import pandas as pd
import os


CITYNAME = '广州'
CID = 20
cities_path = os.path.dirname(os.path.realpath(__file__)) + '/utils/cities.json'
areas_path = os.path.dirname(os.path.realpath(__file__)) + '/utils/guangzhou_area.json'

with open(cities_path, encoding='utf-8') as f:
    CITIES = eval(f.read())
AREAS = []
with open(areas_path, encoding='utf-8') as f:
    tmp = eval(f.read())
    for item in tmp:
        for sub_item in item["subAreas"]:
            if sub_item["name"] != "全部":
                sub_item["parent_id"] = item["id"]
                sub_item["parent_name"] = item["name"]
                AREAS.append(sub_item)

# BASE_URL = "https://{}.meituan.com/meishi/api/poi/getPoiList?".format(CITIES[CITYNAME])
BASE_URL = "http://meishi.meituan.com/i/api/channel/deal/list"
# USER-AGENT
log_path = os.path.dirname(os.path.realpath(__file__)) + '/utils/ua.log'
df = pd.read_csv(log_path, sep='\t')
user_agent = df["UA"].iloc[random.randint(0,1000)]

HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36',
    'Referer': 'http://meishi.meituan.com/i/?ci={}&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1'.format(CID),
}

# UUID
uuid_path = os.path.dirname(os.path.realpath(__file__)) + '/utils/uuid.log'
with open(uuid_path) as f:
    UUID = f.read()

COOKIES = {"ci": "{}".format(CID), "cityname": "%E5%B9%BF%E5%B7%9E"}
REQUEST_PAYLOAD = {
    "uuid": UUID,
    "version": "8.2.0",
    "platform": 3,
    "app": "",
    "partner": 126,
    "riskLevel": 1,
    "optimusCode": 10,
    "originUrl": "http://meishi.meituan.com/i/?ci={}&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1".format(CID),
    "offset": 0, # 偏移量 每次偏移15
    "limit": 15, # 每次获取数量
    "cateId": 1, # 菜式类型
    "lineId": 0,
    "stationId": 0,
    "areaId": 1065, # 地区类型 ，默认0为附近商家
    "sort": "default",  # "default": "智能排序", "distance": "离我最近", "avgscore": "好评优先", "solds": "人气最高",
    "deal_attr_23": "", # 107: "只看免预约"
    "deal_attr_24": "", # 109: "节假日可用"
    "deal_attr_25": "", # 115: "单人餐", 117: "双人餐", 111: "3-4人餐", 112: "5-10人餐", 110: "10人餐以上"
    "poi_attr_20043": "", # 20122: "早餐" , 20123: "午餐", 20124:"下午茶", 20125: "晚餐", 20126: "夜宵"
    "poi_attr_20033": "" # 20062: "买单", 20063: "在线点菜", 20064: "外卖送餐", 20065: "在线排队", 20135: "预定"
}

DATA = {
    "cityName": CITYNAME,
    "cateId": '0',
    "areaId": "0",
    "sort": "",
    "dinnerCountAttrId": "",
    "page": "1",
    "userId": "",
    "uuid": UUID,
    # "uuid": "5a794ab1247b427fb2c8.1556452305.1.0.0",
    "platform": "1",
    "partner": "126",
    "originUrl": "https://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
    "riskLevel": "1",
    "optimusCode": "1"
}

# GET PARAMETER
GET_PARAM =  {
        "cityName": DATA["cityName"],
        "cateId": DATA["cateId"],
        "areaId": DATA["areaId"],
        "sort": DATA["sort"],
        "dinnerCountAttrId": DATA["dinnerCountAttrId"],
        "page": DATA["page"],
        "userId": DATA["userId"],
        "uuid": DATA["uuid"],
        "platform": DATA["platform"],
        "partner": DATA["partner"],
        "originUrl": DATA["originUrl"],
        "riskLevel": DATA["riskLevel"],
        "optimusCode": DATA["optimusCode"],
        # "_token": encrypt_token()
}

# SIGN PARAMETER
SIGN_PARAM = "areaId={}&cateId={}&cityName={}&dinnerCountAttrId={}&optimusCode={}&originUrl={}&page={}&partner={}&platform={}&riskLevel={}&sort={}&userId={}&uuid={}".format(
    DATA["areaId"],
    DATA["cateId"],
    DATA["cityName"],
    DATA["dinnerCountAttrId"],
    DATA["optimusCode"],
    DATA["originUrl"],
    DATA["page"],
    DATA["partner"],
    DATA["platform"],
    DATA["riskLevel"],
    DATA["sort"],
    DATA["userId"],
    DATA["uuid"]
)

# TIME OUT
TIMEOUT = 5

# MAX PAGES
LIMIT = 15

# MYSQL SETTINGS
HOST = 'localhost'
USER = 'root'
PASS = '123456'
PORT = 3306
DB = 'mtdb'
TABLE = 'meishi'

# PROXY API
API = ''

# PROXY SETTINGS
PROXY_HOST = "http-dyn.abuyun.com"
PROXY_PORT = "9020"
PROXY_USER = "HU4C31nmfiDR57D"
PROXY_PASS = "2D4F3B8489F5FC91"

if __name__ == '__main__':
    # print(os.path.dirname(os.path.realpath(__file__)))
    pass
    # print(len(AREAS))
    # print(AREAS)
