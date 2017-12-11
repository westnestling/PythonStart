import datetime
import time
import json
import re
from urllib import request

#抓去万年历数据
begin = datetime.date(2019, 12, 1)
end = datetime.date(2020, 12,1)

url = 'http://tools.2345.com/frame/api/GetLunarInfo?date='
# request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')


d = begin
delta = datetime.timedelta(days=1)
output = open('CalenderData'+begin.strftime("%Y%m%d")+'_'+end.strftime("%Y%m%d")+'.txt', 'w+')
output.write("[")
while d <= end:
    print(d.strftime("%Y%m%d"))
    response = request.urlopen(url + d.strftime("%Y%m%d"))
    #获取数据并抽取
    data = response.read().decode('utf-8')
    # 时间
    pDay = r"\d{4}-\d{2}-\d{2}"
    pattern1 = re.compile(pDay)
    # 农历 天干地支
    pTGDZ = r"[^\d]{3}年 [^\d]*月 [^\d]*?日"
    pTGDZPattern = re.compile(pTGDZ)
    # 农历月
    pTroYear = r"农历.+年[^ ]+"
    pTroYearPattern = re.compile(pTroYear)
    # 适宜
    pYi = r"yi:\".+?[\"]"
    pYiPattern = re.compile(pYi)
    # 生肖
    pAni = r"生肖属[\D]"
    pAniPattern = re.compile(pAni)

    result = ["{\"time\":\"",pattern1.findall(data)[0],'\",',
              "\"chineseYear\":\"",pTGDZPattern.findall(data)[0][0:2]+'年','\",',
              "\"era\":\"",pTGDZPattern.findall(data)[0][5:],'\",',
              "\"day\":\"",pTroYearPattern.findall(data)[0][7:],'\",',
              "\"animal\":\"",pAniPattern.findall(data)[0][-1],'\",',
              "\"nice\":\"",pYiPattern.findall(data)[0][4:-1],'\"','}']
    output.write(''.join(result))
    d += delta
    if d<=end:
        output.write(",")
output.write("]")
output.close()
