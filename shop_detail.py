import requests
import json
import os

# cookies = {
#     "ci": "1",  # 城市代码
#     "cityname": "%E5%8C%97%E4%BA%AC"  # 城市名称
# }
cookies = {"ci": "20", "cityname": "%E5%B9%BF%E5%B7%9E"}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36',
    'Referer': 'http://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
}
demo_path = os.path.dirname(os.path.realpath(__file__)) + '/utils/demo.json'
with open(demo_path, encoding='utf-8') as f:
    DEMO_RESPONSE = eval(f.read())
poiInfos = DEMO_RESPONSE['data']['poiList']['poiInfos']
for poiInfo in poiInfos:
    ctPoi = poiInfo['ctPoi']
    poiid = poiInfo['poiid']
    cateName = poiInfo['cateName']
    name = poiInfo['name']
    city = cookies['cityname']
    detail_url = f'https://meishi.meituan.com/i/poi/{poiid}?ct_poi={ctPoi}'
    print(detail_url)
    res = requests.get(
        url=detail_url,
        headers=headers,
        cookies=cookies,
    )
    # with open('./'+name+'.html', "w", encoding='utf-8') as f:
    #     f.write(res.text)
    print(res.text)
    break