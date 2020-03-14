import pandas as pd
import numpy as np
import datetime
import json
from os import path

province_list = ['湖北','上海','北京','四川','广东','云南','天津','山东','河南','浙江','重庆','黑龙江','宁夏',
                  '安徽','山西','广西','江苏','江西','河北','海南','湖南','福建','贵州','辽宁','内蒙古','吉林','新疆',
                  '甘肃','陕西','青海','西藏','香港','澳门','台湾']

base_path = './DXY-COVID-19-Data/csv/'

cov_data = pd.read_csv(path.join(base_path,'DXYArea.csv'))
cov_data['updateTime'] = pd.to_datetime(cov_data.updateTime).dt.date
cov_data['provinceName'] = cov_data.provinceName.str.replace(r'省|市|(回族|壮族|维吾尔)*自治区','')
cov_data = cov_data[cov_data.provinceName.isin(province_list)]
cov_data = cov_data.drop_duplicates(['provinceName','updateTime']).reset_index(drop=True)
cov_data = cov_data[['provinceName','province_confirmedCount','province_curedCount','province_deadCount','updateTime']]

cov_sum_province = cov_data.drop_duplicates(['provinceName'],keep='first').reset_index(drop=True).drop(['updateTime'],axis=1)
cov_sum_province = cov_sum_province.rename(columns={'provinceName':'province','province_confirmedCount':'confirmed','province_curedCount':'cured','province_deadCount':'death'})

stat = pd.read_csv('./externalData/stat.csv')
stat = pd.merge(stat,cov_sum_province,on=['province'],how='right')
stat['curedRate'] = stat.cured / stat.confirmed
stat['healthStaffPer10w'] = ( stat.healthTechPersonNumber * 10000) / (stat.population / 10)
stat[['province','population','bedUsageRate','transportTotal','healthStaffPer10w','confirmed','cured','death']].fillna(-1).to_csv('./public/data/overall.stat.csv',index=False)

dateObj = {
    'thePaperData':cov_data.updateTime.max().strftime('%Y-%m-%d'),
    'theOverallData': '2018'
}
str = json.dumps(dateObj,ensure_ascii=False)
with open('./public/data/overall.stat.date.json','w') as file:
    file.write(str)
    file.close()

