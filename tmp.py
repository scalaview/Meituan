import requests
import json

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36',
    'Referer': 'http://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
}

request_payload = {
    "uuid": "106aa05a-ff4e-43bf-85e7-8c0a093b1473",
    "version": "8.2.0",
    "platform": 3,
    "app": "",
    "partner": 126,
    "riskLevel": 1,
    "optimusCode": 10,
    "originUrl": "http://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
    "offset": 15, # 偏移量 每次偏移15
    "limit": 1, # 每次获取数量
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
url = 'https://meishi.meituan.com/i/api/channel/deal/list'

cookies = {"ci": "20", "cityname": "%E5%B9%BF%E5%B7%9E"}
response = requests.post(url, data=json.dumps(request_payload), headers=headers, cookies=cookies)
list_data = json.loads(response.text)
print(list_data)