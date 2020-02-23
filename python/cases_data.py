import pandas as pd
import numpy as np
import json


def proc_date(value):
    if isinstance(value, str) and not value.startswith('20'):
        return np.nan
    else:
        return value


def start_place(value):
    if value.startswith('长居'):
        return value.replace('长居','') + '市'
    else:
        return '武汉市'

cases = pd.read_csv('./externalData/NC_763_Cases_Plain.csv')
cases['出发地'] = cases['到达武汉时间'].apply(start_place)

date_proc_fields = ['确诊时间','到达武汉时间','离开武汉日期（或离开其他地区日期）','出现症状时间','首次入院/就诊时间']
for field in date_proc_fields:
    cases[field]=pd.to_datetime(cases[field].apply(proc_date)).dt.date
cases = cases.drop(['联系（人传人）'],axis=1)
cases['症状间隔'] = (cases['出现症状时间'] - cases['到达武汉时间']).apply(lambda value: value.days)
cases['入院间隔'] = (cases['首次入院/就诊时间'] - cases['出现症状时间']).apply(lambda value: value.days)
cases['入院间隔'] = cases['入院间隔'].apply(lambda value: 0 if value < 0 else value)
cases['曾到达武汉'] = cases.apply(lambda row: True if (row['经过地1'] == '武汉市' or row['经过地2'] == '武汉市' or row['经过地3'] == '武汉市' or row['经过地4'] == '武汉市') else False,axis=1)


cases_export = cases[['人传人（疑似）','是否死亡','性别','年龄','类型（人传人）','症状间隔','入院间隔']]
cases_export = cases_export.fillna('')
cases_export.to_csv('./public/data/cases.data.csv',index=False)

cases_have_been_wh = cases[cases['曾到达武汉']].reset_index(drop=True)[['经过地1','经过地2','经过地3','经过地4']]

step_list = []
nodes = []
for index,row in cases_have_been_wh.iterrows():
    have_been_WH = False
    step = 1
    for i in range(1,4):
        if row['经过地'+str(i)] is np.nan:
            break
        if row['经过地'+str(i)].startswith('武汉'):
            have_been_WH = True
        if have_been_WH and row['经过地'+str(i+1)] is not np.nan:
            step_list.append([row['经过地'+str(i)],row['经过地'+str(i+1)],1])
            step += 1

route_table = pd.DataFrame(step_list,columns=['source','target','value']).groupby(['source','target']).sum().reset_index()
city_set = np.union1d(route_table.source.unique(),route_table.target.unique())
target_cnt = route_table.groupby('target').sum().reset_index().sort_values(by=['value']).reset_index(drop=True)

for city in city_set:
    tmp = target_cnt[target_cnt.target == city]
    if len(tmp) > 0:
        size = tmp.iloc[0]['value']
    else:
        size = 1
    nodes.append({'name':city,'value':int(size)})
    
    
json_str = route_table[(route_table['source'] != route_table['target'])].to_json(orient='records',force_ascii=False)
json_obj = {
    'edges':json.loads(json_str),
    'nodes':nodes
}
json_str = json.dumps(json_obj,ensure_ascii=False)

with open('./public/data/cases.routes.json','w') as file:
    file.write(json_str)
    file.close()

