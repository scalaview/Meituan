function importJS(url) {
  var importJs=document.createElement('script')
  importJs.setAttribute("type","text/javascript")
  importJs.setAttribute("src", url)
  document.getElementsByTagName("head")[0].appendChild(importJs)
}

function getRandomArbitrary(min, max) {
  return Math.round(Math.random() * (max - min) + min);
}

importJS('https://ajax.aspnetcdn.com/ajax/jQuery/jquery-2.1.1.min.js')

areaObj = Object.values(window._appState.navBarData.areaObj).reverse()
// areaObj.pop()
// areaObj.reverse()
areas = areaObj.flat().filter(function(e){ return e.name != '全部'; }).reverse()
crawlerMeta = window._appState.crawlerMeta
finishMeituan = window.localStorage.getItem('finish-meituan')
if (finishMeituan == undefined){
  finishMeituan = '[]'
  window.localStorage.setItem('finish-meituan', finishMeituan)
}
finishMeituan = JSON.parse(finishMeituan)
area = areas.pop()
while(true){
  if(finishMeituan.indexOf(area.id) != -1){
    console.log("areaId: " + area.id + " 已经抓取过，获取下个id")
    area = areas.pop()
  } else {
    break
  }
}

offset = 0
total = 1
limit = 50
areaId = area.id
window.localStorage.removeItem('meituan-'+ areaId, '')
result = []

function crawl(){
  if (offset >= total){
    console.log("area: " + areaId + " 抓取完毕")
    finishMeituan = window.localStorage.getItem('finish-meituan')
    finishMeituan = JSON.parse(finishMeituan)
    finishMeituan.push(areaId)
    window.localStorage.setItem('finish-meituan', JSON.stringify(finishMeituan) )
    if (areas.length > 0){
      area = areas.pop()
      areaId = area.id
      offset = 0
      total = 1
      result = []
      window.localStorage.setItem('meituan-'+ areaId, '')
    } else {
      clearInterval(crawlTask)
      return
    }
  }
  params = Object.assign({
    "uuid":"4a3eade9109047ec82f3.1611732056.1.0.0",
    "version":"8.2.0",
    "platform":3,
    "app":"",
    "partner":126,
    "riskLevel":1,
    "optimusCode":10,
    "originUrl":"http://meishi.meituan.com/i/?ci=20&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
    "offset": offset,
    "limit": limit,
    "cateId":1,
    "lineId":0,
    "stationId":0,
    "areaId": areaId,
    "sort":"default",
    "deal_attr_23":"",
    "deal_attr_24":"",
    "deal_attr_25":"",
    "poi_attr_20043":"",
    "poi_attr_20033":""
  }, crawlerMeta)
  jQuery.ajax({
    method: "POST",
    url: "https://meishi.meituan.com/i/api/channel/deal/list",
    data: params
  }).success(function(res) {
    if (res.data && res.data.poiList) {
      total = res.data.poiList.totalCount
      console.log("total: "+ total + " already get: " + (offset + res.data.poiList.poiInfos.length) + " fetch: "+ areaId + " result: " + res.data.poiList.poiInfos.length)
      if(res.data.poiList.poiInfos.length > 0){
        result = result.concat(res.data.poiList.poiInfos)
      }
      window.localStorage.setItem('meituan-'+ areaId, JSON.stringify(result));
      offset = offset + limit
    } else {
      console.log("没有数据")
      console.log(res)
      clearInterval(crawlTask)
    }
  }).fail(function(err){
    console.log(err)
  })
  // clearInterval(crawlTask)
}

crawlTask = setInterval(crawl, getRandomArbitrary(60, 120) * 1000)


// finishMeituan = window.localStorage.getItem('finish-meituan')
// finishMeituan = JSON.parse(finishMeituan)
// allResult = []
// finishMeituan.forEach(function(e) {
//   allResult = allResult.concat(JSON.parse(window.localStorage.getItem('meituan-'+ e)))
// })