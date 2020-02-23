import pandas as pd
import numpy as np
import datetime
import json

province_list = ['湖北','上海','北京','四川','广东','云南','天津','山东','河南','浙江','重庆','黑龙江','宁夏',
                  '安徽','山西','广西','江苏','江西','河北','海南','湖南','福建','贵州','辽宁','内蒙古','吉林','新疆',
                  '甘肃','陕西','青海','西藏','香港','澳门','台湾']

today = datetime.date.today() 
currTimeTs = pd.Timestamp(today)

def cleanTimeError(date):
    if date >= currTimeTs:
        return currTimeTs
    else:
        return date

path = './Novel-Coronavirus-Updates/Updates_NC.csv'
try:
    cov_data = pd.read_csv(path,encoding="utf8")
except:
    cov_data = pd.read_csv(path, encoding="gb2312")

cov_data = cov_data.rename(columns={
    '报道时间':'report_date','省份':'province','城市':'city','新增确诊':'confirmedIncr',
    '新增出院':'curedIncr','新增死亡':'deathIncr','消息来源':'source','来源链接1':'link1',
    '来源链接2':'link2','来源链接3':'link3'
})
cov_data = cov_data[cov_data.province.isin(province_list)]
cov_data['report_date'] = pd.to_datetime(cov_data.report_date.apply(lambda x:u'2020年'+ x ),format=u'%Y年%m月%d日')
cov_data['report_date'] = cov_data.report_date.apply(cleanTimeError)
cov_data = cov_data[cov_data['report_date'].notnull()][['province','report_date','confirmedIncr','curedIncr','deathIncr']]
cov_sum_province = cov_data.groupby(['province']).sum().reset_index()
cov_sum_province = cov_sum_province.rename(columns={'confirmedIncr':'confirmed','curedIncr':'cured','deathIncr':'death'})

stat = pd.read_csv('./externalData/stat.csv')
stat = pd.merge(stat,cov_sum_province,on=['province'],how='right')
stat['curedRate'] = stat.cured / stat.confirmed
stat['healthStaffPer10w'] = ( stat.healthTechPersonNumber * 10000) / (stat.population / 10)
stat[['province','population','bedUsageRate','transportTotal','healthStaffPer10w','confirmed','cured','death']].fillna(-1).to_csv('./public/data/overall.stat.csv',index=False)

dateObj = {
    'thePaperData':cov_data.report_date.max().strftime('%Y-%m-%d'),
    'theOverallData': '2018'
}
str = json.dumps(dateObj,ensure_ascii=False)
with open('./public/data/overall.stat.date.json','w') as file:
    file.write(str)
    file.close()

