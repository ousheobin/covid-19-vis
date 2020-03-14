import pandas as pd
import numpy as np
import datetime
import json
from os import path

province_list = ['湖北省','上海市','北京市','四川省','广东省','云南省','天津市','山东省','河南省','浙江省','重庆市','黑龙江省','宁夏回族自治区',
                  '安徽省','山西省','广西壮族自治区','江苏省','江西省','河北省','海南省','湖南省','福建省','贵州省','辽宁省','内蒙古自治区','吉林省',
                  '新疆维吾尔自治区','甘肃省','陕西省','青海省','西藏自治区','香港','澳门','台湾']

base_path = './DXY-COVID-19-Data/csv/'

cov_data = pd.read_csv(path.join(base_path,'DXYArea.csv'))
cov_data['updateTime'] = pd.to_datetime(cov_data.updateTime).dt.date
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

