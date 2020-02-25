import pandas as pd
import numpy as np
import json
import time
from os import path
import jieba
import jieba.analyse

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

jieba.suggest_freq('新冠肺炎', True)
jieba.suggest_freq('新冠病毒', True)
jieba.suggest_freq('奥司他韦', True)

stop_words = []
with open('./externalData/stopwords.txt','r') as file:
    words = file.read()
    stop_words = words.split('\n')

dxy_base_path = './DXY-COVID-19-Data/csv/'
dxy_rumors = pd.read_csv(path.join(dxy_base_path,'DXYRumors.csv'))

baidu_index = pd.read_csv('./externalData/baidu.index.csv')
weibo_index = pd.read_csv('./externalData/weibo.index.csv')

word_list = []
for title in dxy_rumors.title:
    tf_idf_list = jieba.analyse.extract_tags(title,topK=7)
    for word in tf_idf_list:
        if word not in stop_words and not is_number(word):
            word_list.append({'keyword':word,'cnt':1})
rumors_word = pd.DataFrame(word_list).groupby(['keyword']).sum().sort_values(by=['cnt'],ascending=False).reset_index()
word_cloud_obj = json.loads(rumors_word[rumors_word.cnt >= 3].to_json(orient='records',force_ascii=False))

index_rate = pd.merge(baidu_index.rename(columns={'武汉':'wuhan_baidu','肺炎':'pneumonia_baidu','口罩':'mask_baidu'}),weibo_index.rename(columns={'武汉':'wuhan_weibo','肺炎':'pneumonia_weibo','口罩':'mask_weibo'}),left_on=['time'],right_on=['date']).drop(['time'],axis=1)

final_series = pd.DataFrame()
final_series['date'] = index_rate['date']

for keyword in ['wuhan','pneumonia','mask']:
    for platform in ['baidu','weibo']:
        key = keyword + '_' + platform
        index_rate[key] = (index_rate[key] - index_rate[key].min()) / (index_rate[key].max() - index_rate[key].min())
    final_series[keyword] = ((index_rate[keyword +'_weibo'] * 0.6 + index_rate[keyword +'_baidu'] * 0.4) * 100).round(2)

json_str = pd.DataFrame({
    'date': final_series['date'],
    'focus': final_series['wuhan'] * 0.2 +  final_series['pneumonia'] * 0.8
}).to_json(orient='records',force_ascii=False)
focus_obj = json.loads(json_str)

json_str = pd.DataFrame({
    'date': final_series['date'],
    'focus': final_series['mask'] * 0.2
}).to_json(orient='records',force_ascii=False)
mask_obj = json.loads(json_str)

overall_data = {
    'wordCloud': word_cloud_obj,
    'focus': focus_obj,
    'mask':mask_obj
}
json_str = json.dumps(overall_data,ensure_ascii=False)

with open('./public/data/media.json','w') as file:
    file.write(json_str)
    file.close()
